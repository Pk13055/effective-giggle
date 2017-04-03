# This file will contain all the functions associated 
# with the routes in the Home folder, so as to keep routing as minimal as possible
from app import db, models
from flask import jsonify
import config


# helper modules required
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from app.models import User
import os, hashlib, datetime

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


def createUser(request):
	try:
		email = request.form["email"]
		institute = request.form["institute"]
		location = request.form["location"]
		password = request.form["password"]
		role = request.form["role"]
		username = request.form["username"]
		
		file = request.files['file0']
		filename = file.filename
		
		if file and '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS_IMAGE:
			filename = hashlib.sha1(datetime.datetime.today().isoformat(':')).hexdigest() + '.' + filename.rsplit('.', 1)[1].lower()
			file.save(os.path.join(config.UPLOAD_FOLDER_IMAGE, filename))
			profile_location = filename
		else:
			profile_location = config.STANDARD_IMAGE

	except KeyError as e:
		return jsonify(success=False, message="%s not sent in the request" % e.args), 400 

	u = User(username, email, password, institute, location, role, profile_location)
	db.session.add(u)
	try:
		db.session.commit()
	except IntegrityError as e:
		return jsonify(success=False, message="This email already exists"), 400		
	return True
