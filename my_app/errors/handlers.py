from flask import Blueprint, render_template

social = {'facebook': ('https://www.facebook.com/fola.ademoye', 'fab fa-facebook-square'),
          'instagram': ('https://www.instagram.com/folaademoye/?hl=en', 'fab fa-instagram'),
          'pinterest': ('https://www.pinterest.co.uk/motivationyoga/', 'fab fa-pinterest-square'),
          'linkedin': ('https://www.linkedin.com/in/fola-ademoye-655a331/', 'fab fa-linkedin')}

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', social=social), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', social=social), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', social=social), 500
