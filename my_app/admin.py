"""
Initialize Admin instance.
Register and customize Flask admin pages.
"""

from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from my_app import app, db, bcrypt
from my_app.models import User
from flask_login import current_user, logout_user, login_required
from datetime import datetime


# overwriting default AdminView
class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('home'))

	@expose('/')
	def index(self):
		now = datetime.now()
		arg1 = now.strftime('%A: %b %d, %Y')
		return self.render('admin/index.html', arg1=arg1)


# overwriting default ModelView
class MyModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('home'))

class MyUserModelView(MyModelView):
	column_exclude_list = []
	column_display_pk = True
	can_create = True
	can_edit = True
	can_delete = True
	create_modal = True

	def on_model_change(self, form, model, is_created):
		# model.password = generate_password_hash(model.password, method='sha256')
		model.password = bcrypt.generate_password_hash(model.password).decode('utf-8')


# Admin Home/Index View
admin = Admin(app, name='MyApp', index_view=MyAdminIndexView(), template_mode='bootstrap3')
admin.add_link(MenuLink(name='Home', url='/'))
admin.add_link(MenuLink(name='Logout', url='/logout'))

# Model Views in admin panel
admin.add_view(MyUserModelView(User, db.session))

