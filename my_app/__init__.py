"""
Init file for basic Flask Admin app with single user login.
Inistances and Imports in a specific order
to avoid cilcular imports.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize instance of databse
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#initialize login manager
login_manager = LoginManager(app)

# admin initialized in admin.py
from my_app.admin import admin

# import routes dependent on initialized app
from my_app import routes
