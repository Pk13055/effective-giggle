import os
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, models 
import helper
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from app.models import User

home = Blueprint('home', __name__)

@home.route('/', methods = ['POST', 'GET'])
def home_render():
	if request.method == 'GET':
		return render_template('Main/home.html')

@home.route('/signin', methods = ['POST', 'GET'])
def signin():
	if request.method == 'GET':
		return render_template('Forms/loginpage.html')
	elif request.method == 'POST':
		return helper.makeJSON(request.form['email'], request.form['username'], request.form['password'])

@home.route('/signup', methods = ['POST', 'GET'])
def signup():
	if request.method == 'GET':
		return render_template('Forms/registration.html')
	elif request.method == 'POST':
		try:
			email = request.form["email"]
			institute = request.form["institute"]
			location = request.form["location"]
			password = request.form["password"]
			role = request.form["role"]
			username = request.form["username"]
			picpath = request.form["picpath"]
			profile_location = username + picpath

		except KeyError as e:
			return jsonify(success=False, message="%s not sent in the request" % e.args), 400 

		u = User(username, email, password, institute, location, role, profile_location)
		db.session.add(u)
		try:
			db.session.commit()
		except IntegrityError as e:
			return jsonify(success=False, message="This email already exists"), 400		
		return render_template('Forms/loginpage.html')
