from flask import render_template, redirect, request, url_for
from my_app import app

@app.route('/')
def home():
	return 'Hello World!'

# @app.route('/login')
# def login():
# 	user = User.query.get(1)
# 	login_user(user)
# 	return 'Logged in'

# @app.route('/logout')
# def logout():
# 	logout_user()
#	return 'Logged out'
