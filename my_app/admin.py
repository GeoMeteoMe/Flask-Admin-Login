"""
Initialize Admin instance.
Register and customize Flask admin pages.
"""

from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from my_app import app, db, bcrypt
from my_app.models import User
from flask_login import current_user, logout_user, login_required


# overwriting default AdminView
class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('home'))

# overwriting default ModelView
class MyModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('home'))

class MyUserModelView(ModelView):
	column_exclude_list = []
	column_display_pk = True
	can_create = True
	can_edit = True
	can_delete = True

	def on_model_change(self, form, model, is_created):
		# model.password = generate_password_hash(model.password, method='sha256')
		model.password = bcrypt.generate_password_hash(model.password).decode('utf-8')


admin = Admin(app, name='My App', index_view=MyAdminIndexView())
admin.add_view(MyUserModelView(User, db.session))
