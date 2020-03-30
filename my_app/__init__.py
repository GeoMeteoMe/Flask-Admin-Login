"""
Init file for basic Flask Admin app with single user login.
Inistances and Imports in a specific order
to avoid cilcular imports.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

#https://support.google.com/mail/answer/7104828?hl=en&visit_id=637211868782626265-231136944&rd=1
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
#app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@my_app.com'
app.config['MAIL_USERNAME'] = 'youremail'
app.config['MAIL_PASSWORD'] = 'yourpassword'


# initialize instance of databse and mail
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

#initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
#login_manager.login_message_category = 'info'

# admin initialized in admin.py
from my_app.admin import admin

# import routes dependent on initialized app
from my_app import routes
