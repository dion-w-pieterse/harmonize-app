from flask import Flask, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

from flask_mail import Mail, Message
from flask_migrate import Migrate
import psycopg2
# Flask-Admin imports
from flask_admin import Admin

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR

class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR

# PugSQL
import pugsql

app = Flask(__name__)
#app.config.from_object(Config)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": '<email address>',
    "MAIL_PASSWORD": '<enter gmail account password here>'
}

app.config['SECRET_KEY'] = '<your secret key>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://<user>:@localhost/<project_name>'
app.config['POSTS_PER_PAGE'] = 8
app.config['ADMINS'] = '<email address>'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config.update(mail_settings)

# create database instance
db = SQLAlchemy(app)
# Take care of Mail
mail = Mail(app)
# create instance of migration instance
migrate = Migrate(app, db)

# instantiate Flask-Admin
admin = Admin(app, template_mode='bootstrap4')

# set up pugsql
queries = pugsql.module('harmonize_package/queries/')

queries.connect('postgresql+psycopg2://dionpieterse:@localhost/project_harmonize')


######################################
#### Additional Flask Login Steps ####
#########################################
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from harmonize_package.models import User
from harmonize_package import routes

# This was added to redirect users to login page if they try access a protected page without being logged in
@login_manager.unauthorized_handler
def unauthorized_handler():
    print(request.full_path)
    session['next'] = request.full_path
    session.modified = True
    return redirect(url_for('login'))