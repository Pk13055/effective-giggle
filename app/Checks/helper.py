from app import db, models
from flask import jsonify
import config

# helper modules required
from sqlalchemy.exc import IntegrityError
from app.models import User

def checkuser(username):
	exists = User.query.filter(User.username==username).count()
	if exists == 0 :
		return True
	else:
		return False

def checkemail(email):
	exists = User.query.filter(User.email==email).count()
	if exists == 0 :
		return True
	else:
		return False
