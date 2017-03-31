import sys, string, os
from random import randint
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import Comment


for _ in range(int(sys.argv[1])):
	user_id = randint(1, 10 ** 5)
	problem_id = randint(1, 10 ** 5)
	body = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(randint(10, 200)))
	db.session.add(Comment(user_id, problem_id, body))

db.session.commit()