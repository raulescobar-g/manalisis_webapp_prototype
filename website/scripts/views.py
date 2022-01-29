from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Receipt
from .. import db
from datetime import datetime
from .helper import file_upload, allowed_file
from flask_mail import Message
from .. import mail


views = Blueprint('views', __name__)

UPLOAD_FOLDER = '/images/'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg'])


#COMMITS RECEIPTS TO DATABASE
@views.route('/user',methods=['POST','GET'])
@login_required
def index():
    if "project_id" in session:
        project_id = session['project_id']

        #IF FORM SUBMITTED THEN FETCH DATA INPUTED 
        if request.method == "POST":
            try:
                file = request.files['im_input']
                place = request.form['place']
                time = request.form['time']
                total = request.form['total']
                iva = request.form['iva']
                cost = request.form['cost']
                rfc = request.form['rfc']
                address = request.form['address']
                phonee = request.form['phonee']
                description = request.form['description']
                proof = request.files['proof']
                proof1 = request.files['proof1']
                proof2 = request.files['proof2']

                if description != '':
                    
                    msg = Message('[OT {}] Solicitud de Viáticos Observaciones'.format(project_id), sender = 'recibos.microanalisis@gmail.com', recipients = ['administracion_vhsa@microanalisis.com','raul3@microanalisis.com','sofia@microanalisis.com'])
                    
                    msg.body = description
                    if proof.filename != "" and allowed_file(proof.filename,ALLOWED_EXTENSIONS):
                        f = proof.read()
                        byte_array = bytearray(f)
                        msg.attach(proof.filename, "image/{}".format(proof.filename[-4:]),data=byte_array)

                    if proof1.filename != "" and allowed_file(proof1.filename,ALLOWED_EXTENSIONS):
                        f = proof1.read()
                        byte_array = bytearray(f)
                        msg.attach(proof1.filename, "image/{}".format(proof1.filename[-4:]),data=byte_array)

                    if proof2.filename != "" and allowed_file(proof2.filename,ALLOWED_EXTENSIONS):
                        f = proof2.read()
                        byte_array = bytearray(f)
                        msg.attach(proof2.filename, "image/{}".format(proof2.filename[-4:]),data=byte_array)
                        
                    mail.send(msg)
                    
                #IF FILE GIVEN THEN SAVE RECEIPT WITH FILE, IF NO FILE GIVEN THEN DO NOT SAVE RECEIPT WITH FILE
                if file.filename != "" and allowed_file(file.filename,ALLOWED_EXTENSIONS):
                    now = datetime.now()
                    filename = str(current_user.id) + now.strftime("_%m.%d.%Y_%H.%M.%S")+ file.filename[-4:]
                        
                    file_upload(file, filename, UPLOAD_FOLDER)

                    receipt = Receipt(rfc=rfc, 
                                        address=address, 
                                        phonee=phonee, 
                                        place = place, 
                                        time = time, 
                                        total= total,
                                        iva=iva, 
                                        cost=cost, 
                                        file_loc = filename,
                                        user=current_user,
                                        project_id=project_id) 
                else:
                    receipt = Receipt(rfc=rfc,
                                        address=address,
                                        phonee=phonee, 
                                        place = place, 
                                        time = time, 
                                        total= total,
                                        iva=iva,
                                        cost=cost,
                                        user=current_user,
                                        project_id=project_id)
            except:
                flash("No hay Orden de Trabajo seleccinado",'info')
                return render_template("index.html",project_name="---")
                
        #IF NOTHING GETS POSTED, RENDER TEMPLATE AS NORMAL
        else:
            return render_template("index.html",project_name=project_id)

        #AFTER RECEIPT IS CREATED, WE ADD AND COMMIT CHANGES THEN RELOAD
        db.session.add(receipt)
        db.session.commit()
        flash('Recibo agregado', category='success')
        return redirect(url_for("views.index"))
        

    #IF SESSION IS OVER REDIRECT TO LOGIN
    else:
        if request.method == "POST":
            flash("No hay Orden de Trabajo seleccinado",'info')
        return render_template("index.html",project_name="---")





