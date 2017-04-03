# This file will contain all the functions associated 
# with the routes in the Home folder, so as to keep routing as minimal as possible
from app import db, models
from flask import jsonify

# helper modules required
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from app.models import User


def makeJSON(email, username, password):
		role = "admin"
		if email:
			auth_id = email
			auth_type = "email"
		else:
			auth_id = username
			auth_type = "username"
		return jsonify({'auth_id' : auth_id, 'auth_type' : auth_type, 'password' : password, 'role' : role})

def makeNewUser(form):
	obj = {}
	for x in form:
		if x != 'submit' and x != 'password_2':
			obj[x] = form[x]
	return jsonify(obj)


def signInUser(request):
	try:
		email = request.form['email']
		password = request.form['password']
	except KeyError as e:
		return jsonify(success = False, message = " %s doesnt exist") % e.args, 400
	user = User.query.filter(User.email == email).first()
	if user is None:
		return jsonify(success = False, message = "Register First"), 401
	elif not user.check_password_hash(password):
		return jsonify(success = False, message = "Wrong Password"), 401
	session['user_uid'] = user.uid
	return jsonify(redirect = '/solver/' + user.uid)

def createUser(request):
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
