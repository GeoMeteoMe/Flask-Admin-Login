"""
Initialize Admin instance.
Register and customize Flask admin pages.
"""

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from my_app import app, db
from my_app.models import User


# overwriting default AdminView
class MyAdminIndexView(AdminIndexView):
	pass
	# def is_accessible(self):
	# 	return current_user.is_authenticated

	# def inaccessible_callback(self, name, **kwargs):
	# 	return redirect(url_for('login'))

# overwriting default ModelView
class MyModelView(ModelView):
	pass
	# def is_accessible(self):
	# 	return current_user.is_authenticated

	# def inaccessible_callback(self, name, **kwargs):
	# 	return redirect(url_for('login'))

class MyUserModelView(ModelView):
	column_exclude_list = []
	column_display_pk = True
	can_create = True
	can_edit = True
	can_delete = False

	def on_model_change(self, form, model, is_created):
		model.password = generate_password_hash(model.password, method='sha256')

admin = Admin(app, name='My App', index_view=MyAdminIndexView())
admin.add_view(MyUserModelView(User, db.session))
