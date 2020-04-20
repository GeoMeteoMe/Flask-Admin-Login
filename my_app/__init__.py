"""
Init file for basic Flask Admin app with single user login.
Inistances and Imports in a specific order
to avoid cilcular imports.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from my_app.config import Config



# create extensions
# justification in flask documentation
# https://youtu.be/Wfx4YBzg16s?t=1973
db = SQLAlchemy()
admin = Admin()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # redirect to after login
login_manager.login_message_category = 'info' #bootstrap info class
mail = Mail()


def create_app(config_class=Config): # default configutation

	app = Flask(__name__)
	app.config.from_object(Config)

	#initialize extensions
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	# customized admin views
	from my_app.models import MyAdminIndexView
	admin.init_app(app,index_view=MyAdminIndexView())#how to add 'name'??
	admin.add_link(MenuLink(name='Home', url='/'))
	admin.add_link(MenuLink(name='Logout', url='/logout'))


	# blueprints
	from my_app.main.routes import main
	from my_app.errors.handlers import errors
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app
