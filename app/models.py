# This is the place to define all models that we need 
# If you access to a particular model please import it as:
#  from models import <class name> 


# imports for the db handling
from app import db
from flask_sqlalchemy import SQLAlchemy


# custom imports required for tasks
import datetime, time
import hashlib
 
# Every problem will be of this type
class Problem(db.Model):
	__tablename__ = 'problems'

	# basic problem identifiers. Try to route using uid, to prevent script attacks
	id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
	uid = db.Column(db.String(255), unique = True, nullable = False)
	title = db.Column(db.String(30), nullable = False)
	tags = db.Column(db.String(255))
	
	# basic info about the problem
	upload_date = db.Column(db.String(255), nullable = False)
	solution_language = db.Column(db.String(10), nullable = False)
	total_submissions = db.Column(db.Integer)
	accepted = db.Column(db.Integer)
	wrong_answer = db.Column(db.Integer)
	tle = db.Column(db.Integer)

	# file locations associated with the problem
	problem_location = db.Column(db.String(300), nullable = False)
	io_location = db.Column(db.String(300), nullable = False)
	solution_location = db.Column(db.String(300), nullable = False)
	editorial_location = db.Column(db.String(300), nullable = False)
	

	def __init__(self, title, tags, problem_location, io_location, solution_language, solution_location, editorial_location):
		
		# data given by the user
		self.title = title
		self.tags = tags
		self.problem_location = problem_location
		self.io_location = io_location
		self.solution_language = solution_language
		self.editorial_location = editorial_location
		self.solution_location = solution_location
		
		# intialized data from backend
		self.total_submissions = self.accepted = self.wrong_answer = self.tle = 0
		self.upload_date = datetime.datetime.today().isoformat(' ')
		self.uid = hashlib.sha1(self.upload_date).hexdigest()


	def __repr__(self):
		"<Problem { 'title' : %s,  'uid' : %s, 'upload_date' : %s, 'tags' : %s } >" % (self.title, self.uid, self.upload_date, self.tags)
		return True


# Every user (solver/setter) will be of this type
class User(db.Model):
	__tablename__ = 'users'
	
	# basic user identifiers. Try to route using uid, to prevent script attacks
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	uid = db.Column(db.String(255), unique = True, nullable = False)
	username = db.Column(db.String(35), unique = True, nullable = False)
	email = db.Column(db.String(60), unique = True, nullable = False)
	role = db.Column(db.String(10), nullable = False)

	# basic info about the user
	password = db.Column(db.String(255), nullable = False)
	institute = db.Column(db.String(255))
	location = db.Column(db.String(255))
	total_submissions = db.Column(db.Integer)
	accepted = db.Column(db.Integer)
	wrong_answer = db.Column(db.Integer)
	tle = db.Column(db.Integer)
	ranking = db.Column(db.String(40), nullable = False, default = "Newbie") 

	# file locations associated with the user
	profile_location = db.Column(db.String(255))


	def __init__(self):
		# insert the assignments here 
		pass

	def __repr__(self):
		# return a readable expression here; this will be called while debugging
		return True

# Every problem submission will be of this type
class Submission(db.Model):
	__tablename__ = 'submissions'
	
	# search using these values
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	submission_timestamp = db.Column(db.DateTime)
	
	# basic info about the submission
	status = db.Column(db.String(50), nullable = False)
	user_id = db.Column(db.String(255), nullable = False)
	problem_id = db.Column(db.String(255), nullable = False)
	submission_language = db.Column(db.String(40), nullable = False)

	def __init__(self):
		# insert the assignments here 
		pass

	def __repr__(self):
		# return a readable expression here; this will be called while debugging
		return True

# Every editorial comment will be of this type
class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	comment_timestamp = db.Column(db.DateTime)
	
	# basic info about the comment 
	user_id = db.Column(db.String(255), nullable = False)
	problem_id = db.Column(db.String(255), nullable = False)
	body = db.Column(db.String(400), nullable = False)

	def __init__(self):
		# insert the assignments here 
		pass

	def __repr__(self):
		# return a readable expression here; this will be called while debugging
		return True