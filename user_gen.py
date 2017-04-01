import sys, string, os
from random import randint
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import User

try:
	db.create_all()
except:
	pass

email_domain = ['gmail', 'yahoo', 'hotmail', 'reddiff', 'outlook']
roles = ['user', 'admin']
for _ in range(int(sys.argv[1])):
	username = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(randint(10, 30)))
	email = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(randint(10, 15))) +  '@' + email_domain[randint(0, len(email_domain) - 1)] + '.com'
	password = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(randint(25,40)))
	location = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(randint(30, 50)))
	institute = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(randint(40, 50)))
	role = roles[randint(0,1)]
	profile_location = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) + '/' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(randint(4, 10))) + '/' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(randint(12,45)))
	db.session.add(User(username, email, password, institute, location, role, profile_location))

db.session.commit()
