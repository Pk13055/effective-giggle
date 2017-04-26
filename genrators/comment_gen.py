import sys, string, os
from random import randint
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import Comment, Problem, User


users = User.query.with_entities(User.uid).all()
user_list = []
for x in users:
	user_list.append(x.uid)

problems = Problem.query.with_entities(Problem.uid).all()
problem_list = []
for x in problems:
	problem_list.append(x.uid)

for _ in range(int(sys.argv[1])):
	user_id = random.choice(user_list)
	problem_id = random.choice(problem_list)
	body = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod \
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, \
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo	\
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse \
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non \
proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
	# print(user_id, problem_id, body)
	db.session.add(Comment(user_id, problem_id, body))

db.session.commit()