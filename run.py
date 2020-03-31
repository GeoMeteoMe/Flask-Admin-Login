#  runs the application

from my_app import create_app

# default configutation is Config (dev).
# overwrite with Config for(prod)
app = create_app()

if __name__ == '__main__':
	app.run(debug=True)
