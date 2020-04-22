from flask import Blueprint
from flask import render_template, url_for, flash, redirect
from flask import request, make_response, session
from my_app import db, mail, bcrypt
from my_app.main.forms import LoginForm, RequestResetForm, ResetPasswordForm
#from my_app.admin import bcrypt
from my_app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


main = Blueprint('main', __name__)

@main.route('/')
@main.route("/home")
def home():
	return render_template('home.html', title='Home')

@main.route('/about')
def about():
	return render_template('about.html', title='About')

@main.route('/cookies')
def cookies():
    res = make_response(render_template('cookies.html', title='Cookies'))

    cookies = request.cookies

    flavor = cookies.get('flavor')
    choc_type = cookies.get('chocolate chip')
    chewy = cookies.get('chewy')

    print('Cookie:::', cookies)
    print('Cookie:::', flavor, choc_type, chewy)

    """
    Parameter	Default	Description
    key     required	The key (name) of the cookie
    value	""	    The value of the cookie
    max_age	None	Number of seconds or None (default)
    expires	None	The date of then the cookie expires, must be a datetime object
    path	None	Limits the cookie to a given path
    domain	None	specify a domain able to read the cookie (default is the domain that set it)
    secure	False	If True, the cookie will only be available over HTTPS
    httponly	False	Disallow JavaScript to access the cookie (Limited browser support)
    samesite	False	Limits the scope of where the cookie is accessible to the same site
    """
    res.set_cookie(
        "flavor",
        value="chocolate chip",
        max_age=10, # in seconds
        expires=None,
        path=request.path,
        domain=None,
        secure=False,
        httponly=False,
        #samesite=False,
        )

    res.set_cookie("chocolate type", "dark")
    res.set_cookie("chewy", "yes")
    return res



# Login/Logout

@main.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    #if user and user.password:
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next') or url_for('admin.index')
      return redirect(next_page) if next_page else redirect(url_for('main.home'))
  return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))



# Password reset

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('main.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@main.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.')
        return redirect(url_for('main.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@main.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token')
        return redirect(url_for('main.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in')
        return redirect(url_for('main.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
