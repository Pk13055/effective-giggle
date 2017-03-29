# This file will contain all the functions associated 
# with the routes in the Home folder, so as to keep routing as minimal as possible
from app import db, models
from flask import jsonify


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
