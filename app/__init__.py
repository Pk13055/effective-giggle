	# Import flask and template operators
from flask import Flask, render_template,session, blueprints,jsonify

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from flask_wtf.csrf import CSRFProtect,CSRFError

from functools import wraps

# Define the WSGI application object
app = Flask(__name__, static_url_path = '/static')

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# csrf protection
csrf=CSRFProtect(app)
@app.errorhandler(CSRFError)
def csrf_error(reason):
    # return jsonify(success=True,error=reason)
    return render_template('error.html', error=reason), 400

# HTTP error handling route
@app.errorhandler(404)
def not_found(error):
	return render_template('error.html', error = error) , 404

# authorization for the logged in state
def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if 'user_uid' not in session:
			return jsonify(success=False, message="Unauthorized entry. Login First"), 400
		return f(*args, **kwargs)
	return decorated

# this function is responsible for cleaning up data parsed from file
def sanitize(data):
	return filter(lambda x: x != '', data)


# Import a module / component using its blueprint handler variable (mod_auth)
from app.Comments.controllers import comments
from app.Home.controllers import home
from app.Problem.controllers import problem
from app.User.controllers import user

# Register blueprint(s)
app.register_blueprint(comments)
app.register_blueprint(home)
app.register_blueprint(problem)
app.register_blueprint(user)


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

