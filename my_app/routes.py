from flask import render_template, url_for, flash, redirect, request
from my_app import app
from my_app.forms import LoginForm
from my_app.admin import bcrypt
from my_app.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
	return render_template('base.html', title='Home')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password')
    return render_template('login.html', title='Login', form=form)


@app.route("/out")
def out():
    return  render_template('out.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('out'))
