import os

class Config:

	SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	#https://support.google.com/mail/answer/7104828?hl=en&visit_id=637211868782626265-231136944&rd=1
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	#MAIL_USE_SSL = True
	MAIL_USE_TLS = True
	MAIL_DEFAULT_SENDER = 'noreply@my_app.com'
	MAIL_USERNAME = 'youremail'
	MAIL_PASSWORD = 'yourpassword'
