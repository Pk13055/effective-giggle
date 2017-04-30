import sys, string, os
from random import randint
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import app 

for _ in range(int(sys.argv[1])):
	user_id = randint(1, 10 ** 5)
	problem_id = randint(1, 10 ** 5)
	body = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(randint(10, 10 ** 4)))
	db.session.add(Problem(user_id, problem_id, body))

db.session.commit()