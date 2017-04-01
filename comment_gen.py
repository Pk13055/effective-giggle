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
	user_id = user_list[randint(0, len(user_list) - 1)]
	problem_id = problem_list[randint(0, len(problem_list) - 1)]
	body = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(randint(10, 200)))
	db.session.add(Comment(user_id, problem_id, body))

db.session.commit()