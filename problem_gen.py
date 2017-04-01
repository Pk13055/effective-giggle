import sys, string
from random import randint
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import Problem, User
try: 
	db.create_all()
except:
	pass

langs = ['C', 'C++', 'python2', 'python3']
uploaders = User.query.filter(User.role == 'admin').with_entities(User.uid).all()
admins = []
for x in uploaders:
	admins.append(x.uid)


for _ in range(int(sys.argv[1])):
	# 	def __init__(self, title, tags, uploader,  problem_location, io_location, 
	# solution_language, solution_location, editorial_location):
	title = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase +  string.digits) for _ in range(randint(10, 50)))
	tag_line = ""
	for j in range(randint(0,10)):
		tag = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase   + string.digits) for _ in range(randint(4,10)))
		tag_line = tag_line + tag + ","
	tag_line = tag_line[:len(tag_line) - 1]
	tags = tag_line
	uploader = admins[randint(0, len(admins) - 1)]
	problem_location = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase   + string.digits) for _ in range(5)) + '/' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(4, 10))) + '/' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(12,45)))
	io_location = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase +   string.digits) for _ in range(5)) + '/' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(4, 10))) + '/' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(12,45)))
	solution_language = langs[randint(0,len(langs) - 1)]
	solution_location = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase   + string.digits) for _ in range(5)) + '/' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(4, 10))) + '/' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(12,45)))
	editorial_location = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase   + string.digits) for _ in range(5)) + '/' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(4, 10))) + '/' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(randint(12,45)))
	db.session.add(Problem(title, tags, uploader, problem_location, io_location, solution_language, solution_location, editorial_location))

db.session.commit()