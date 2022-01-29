from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import  manalisis_Users
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db, mail
from flask_login import login_user, login_required, logout_user, current_user
from .helper import names_list
from itsdangerous import SignatureExpired, BadTimeSignature
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os
load_dotenv()

auth = Blueprint('auth', __name__)
s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

@auth.route('/',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user_search = manalisis_Users.query.filter_by(email=email).first()
        if 'project_id' in session:
            session.pop("project_id",None)
        if user_search is not None:
            if check_password_hash(user_search.password, password):
                
                login_user(user_search, remember=True)
                return redirect(url_for("views.index"))
            else:
                flash("Contrasena equivocada","error")
        else:
            flash("Usuario no existe en nuestra base de datos","error")
        
    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    session.pop("project_id",None)
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/acct_creation',methods=['POST','GET'])
def acct_creation():
    
    if request.method == "POST":
        user = request.form['email']
        password = request.form['password']
        password_check = request.form['password_check']
        if password != password_check:
            flash('Contrasenas no son iguales!', category='error')
            return render_template("acct.html")

        name = request.form['name']
        phone = request.form['phone']

        all_users = manalisis_Users.query.all()
        for i in range(len(all_users)):
            if name == all_users[i].name or user == all_users[i].email:
                flash("Usuario ya existe con ese nombre o email en nustra base de datos",'info')
                return render_template("acct.html")


        new_user = manalisis_Users(email=user
                        ,password=generate_password_hash(password, method='sha256'),
                        name=name,
                        phone=phone)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.name_confirmation",user_id=new_user.id))
        
    else:
        return render_template("acct.html")

@auth.route('/name_confirmation/<int:user_id>',methods=['POST','GET'])
def name_confirmation(user_id):
    user = manalisis_Users.query.filter_by(id=user_id).first()

    if request.method == "POST":
        try:
            name = request.form['name']
            user.name = name
            db.session.commit()
            flash('Cuenta creada!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('proj_view.project_view'))
        except:
            db.session.delete(user)
            db.session.commit()
            flash("Intenta solo usar su primer nombre en Razon Social",'info')
            return redirect(url_for('auth.acct_creation'))
    else:
        names = names_list(user.name)
        if len(names) == 0:
            db.session.delete(user)
            db.session.commit()
            flash("No encontramos un usuario con ese nombre en nuestra base de datos intenta solo el primer nombre",'info')
            return redirect(url_for('auth.acct_creation'))

        return render_template('name_sel.html',user_id=user_id,names=names)


@auth.route('/password',methods=['POST','GET'])
def password():
    if request.method == 'POST':
        email = request.form['email']
        user = manalisis_Users.query.filter_by(email=email).first()
        if user is not None:
            token = s.dumps(email,salt='email-confirm')
            msg = Message("Cambio de Contraseña",
                        sender = 'recibos.microanalisis@gmail.com',
                        recipients = [email]) #change title
            link = url_for('auth.confirm_email',token=token,_external=True)
            msg.body = 'Apretar el link para cambiar su contrasena -> {}'.format(link)
            mail.send(msg)

            flash("Link para cambiar la contraseña se puede encontrar en su email",'success')
            return redirect(url_for('auth.login'))
        else:
            flash("Usuario con este email no existe en nuestra base de datos",'error')
            return redirect(url_for('auth.password'))
    else:
        return render_template('password.html')


@auth.route('/confirm_email/<token>',methods=['POST','GET'])
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=1800)
    except SignatureExpired or BadTimeSignature:
        flash("Wrong token or token expired after 30 minutes of inactivity",'error')
        return redirect(url_for('auth.password'))

    if request.method == 'POST':
        new_pass1 = request.form['new_pass1']
        new_pass2 = request.form['new_pass2']
        if new_pass1 == new_pass2:
            user = manalisis_Users.query.filter_by(email=email).first()
            user.password = generate_password_hash(new_pass1, method='sha256') 
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash("Contrasenas no son iguales",'error')
            return render_template("password_change.html",token=token)
    else:
        return render_template("password_change.html",token=token)