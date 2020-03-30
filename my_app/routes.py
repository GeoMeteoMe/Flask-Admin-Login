from flask import render_template, url_for, flash, redirect, request
from my_app import app, db, mail
from my_app.forms import LoginForm,  RequestResetForm, ResetPasswordForm
from my_app.admin import bcrypt
from my_app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route('/')
def home():
	return render_template('base.html', title='Home')

@app.route('/about')
def about():
	return render_template('about.html', title='About')


# Login/Logout

@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    #if user and user.password:
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next') or url_for('admin.index')
      return redirect(next_page) if next_page else redirect(url_for('home'))
  return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# Password reset

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
