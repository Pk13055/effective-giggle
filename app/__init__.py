# Import flask and template operators
from flask import Flask, render_template, blueprints

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__, static_url_path = '/static')

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error = error) , 404

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
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()