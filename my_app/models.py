"""
Creates basic User table in db.
Loads current user
"""
from datetime import datetime
from flask import current_app, redirect, url_for
from my_app import db, bcrypt, login_manager, admin
from flask_login import UserMixin, current_user, logout_user, login_required
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from my_app.config import Config


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
				user_id = s.loads(token)['user_id']
		except:
				return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', {self.email}, {self.password})"

# CREATE CUSTOM ADMIN VIEWS

class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('main.home'))

	@expose('/')
	def index(self):
		now = datetime.now()
		arg1 = now.strftime('%A: %b %d, %Y')
		return self.render('admin/index.html', arg1=arg1)

class MyModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('main.home'))

class MyUserModelView(MyModelView):
	column_exclude_list = []
	column_display_pk = True
	can_create = True
	can_edit = True
	can_delete = True
	create_modal = True

	def on_model_change(self, form, model, is_created):
		model.password = bcrypt.generate_password_hash(model.password).decode('utf-8')

# register views
admin.add_view(MyUserModelView(User, db.session))
