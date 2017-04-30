import sys, string, os, hashlib
from random import randint
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import User
import config

try:
	db.create_all()
except:
	pass


emails = open(os.path.join(config.UPLOAD_FOLDER_DATASET,'emails.txt')).read().split('\n')[:-1]
names = open(os.path.join(config.UPLOAD_FOLDER_DATASET,'names.txt')).read().split('\n')[:-1]
roles = ['user', 'admin']
places = open(os.path.join(config.UPLOAD_FOLDER_DATASET,'place_list.txt')).read().split('\n')[:-1]


for _ in range(int(sys.argv[1])):
	username = random.choice(names) + str(random.randint(1, 10 ** 9))
	email = username + '@' + random.choice(emails)
	password = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(randint(25,40)))
	location = random.choice(places)
	institute = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(randint(1, 10))) + \
					' ' + ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(randint(1, 10))) + \
					' ' + ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(randint(1, 10))) + \
					' ' + 'University'
	role = random.choice(roles)
	profile_location = hashlib.sha1(username).hexdigest() + '.' + random.choice(list(config.ALLOWED_EXTENSIONS_IMAGE))
	# print(username, email, password, institute, location, role, profile_location)
	db.session.add(User(username, email, password, institute, location, role, profile_location))

db.session.commit()
