from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
import cx_Oracle
from flask_mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
mail = Mail()

def create_app():
    
    oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@' + cx_Oracle.makedsn('{hostname}', '{port}', service_name='{service_name}')
    cx_Oracle.init_oracle_client(lib_dir = os.getenv("ORACEL_DIR"))

    app = Flask(__name__,static_folder='./static',template_folder='templates')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = oracle_connection_string.format(username=os.getenv("USERNAME"),
                                                                            password=os.getenv("PASSWORD"),
                                                                            hostname=os.getenv("HOSTNAME"),
                                                                            port=os.getenv("PORT"),
                                                                            service_name=os.getenv("SERVICE_NAME"))

    app.config['SQLALCHEMY_ECHO'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800
    
    app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_SUPPRESS_SEND'] = False

    db.init_app(app)
    mail.init_app(app)

    from .scripts.models import manalisis_Users
    from .scripts.views import views
    from .scripts.auth import auth
    from .scripts.proj import proj
    from .scripts.xml import xml
    from .scripts.tabulate import tabulate
    from .scripts.proj_view import proj_view

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(proj, url_prefix='/')
    app.register_blueprint(xml, url_prefix='/')
    app.register_blueprint(tabulate, url_prefix='/')
    app.register_blueprint(proj_view, url_prefix='/')


    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return manalisis_Users.query.get(int(id))

    return app

def create_database(app):
    db.create_all(app=app)
