import sys, string, hashlib, datetime, os
from random import randint
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import Problem, User
import config
try: 
	db.create_all()
except:
	pass
 
langs = ['C', 'C++', 'python2', 'python3']
tags = open(os.path.join(config.UPLOAD_FOLDER_DATASET,'tags.txt')).read().split('\n')[:-1]
tags = [i.encode('utf-8') for i in tags]
x = open(os.path.join(config.UPLOAD_FOLDER_DATASET,'problem_names.txt')).read().split('\n')[:-1]
titles = []
for _ in x:
	try:
		titles.append(_.encode('utf-8'))
	except:
		pass
uploaders = User.query.filter(User.role == 'admin').with_entities(User.uid).all()
admins = []
for x in uploaders:
	admins.append(x.uid)


for _ in range(int(sys.argv[1])):
	title = random.choice(titles)
	tag = ','.join(list(set([random.choice(tags) for i in range(random.randint(1,5))])))
	uploader = random.choice(admins)
	current_key = datetime.datetime.today().isoformat(' ').encode('utf-8')
	problem_location = hashlib.sha1(current_key).hexdigest() + '.' + random.choice(list(config.ALLOWED_EXTENSIONS_PROBLEM))
	io_location = hashlib.sha1(current_key).hexdigest() + '.' + random.choice(list(config.ALLOWED_EXTENSIONS_TEST))
	solution_language = random.choice(langs)
	solution_location = hashlib.sha1(current_key).hexdigest() + '.' + random.choice(list(config.ALLOWED_EXTENSIONS_SOLUTION_CODE))
	editorial_location = hashlib.sha1(current_key).hexdigest() + '.' + random.choice(list(config.ALLOWED_EXTENSIONS_EDITORIAL))
	# print(title, tag, uploader, problem_location, io_location, solution_language, solution_location, editorial_location)
	db.session.add(Problem(title, tag, uploader, problem_location, io_location, solution_language, solution_location, editorial_location))

db.session.commit()
# problems=Problem.query.all()
# print(problems)
