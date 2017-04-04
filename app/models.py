# This is the place to define all models that we need 
# If you access to a particular model please import it as:
#  from models import <class name> 


# imports for the db handling
from app import db
from flask_sqlalchemy import SQLAlchemy

#for making hash of password 
from werkzeug.security import generate_password_hash,check_password_hash

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
	uploader = db.Column(db.String(255), nullable = False)
	
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
	

	def __init__(self, title, tags, uploader, problem_location, io_location, solution_language, solution_location, editorial_location):
		
		# data given by the user
		self.title = title
		self.tags = tags
		self.uploader = uploader
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
		return "<Problem { 'title' : %s,  'uid' : %s, 'upload_date' : %s, 'tags' : %s } >" % (self.title, self.uid, self.upload_date, self.tags)

	def getIdentifiers(self):
		return { 'title' : self.title, 'tags' : self.tags, 'upload_date' : self.upload_date }

	def getAssocFiles(self):
		return { 'problem_location' : self.problem_location, 'io_location' : self.io_location, 
					'editorial_location' : self.editorial_location, 'solution_location' : self.solution_location, 
					'solution_language' : self.solution_language
				}

	def getStats(self):
		return {  'total_submissions' : self.total_submissions, 'accepted' : self.accepted, 
					'wrong_answer' : self.wrong_answer, 'tle' : self.tle				
				}

	def getTimeStamp(self):
		return datetime.datetime.strptime(self.upload_date, "%Y-%m-%d %H:%M:%S.%f")



# Every user (solver/setter) will be of this type
class User(db.Model):
	__tablename__ = 'users'
	
	# basic user identifiers. Try to route using uid, to prevent script attacks
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	uid = db.Column(db.String(255), unique = True, nullable = False)
	username = db.Column(db.String(30), unique = True, nullable = False)
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
	rank_value = db.Column(db.Integer, nullable = False, default = 1500)

	
	# file locations associated with the user
	profile_location = db.Column(db.String(255))


	def __init__(self, username, email, password, institute, location, role, profile_location):
		self.username = username
		self.email = email
		self.institute = institute
		self.location = location
		self.profile_location = profile_location
		self.role = role
		self.total_submissions = self.accepted = self.wrong_answer = self.tle = 0
		self.uid = hashlib.sha1(datetime.datetime.today().isoformat(' ')).hexdigest()
		self.password = generate_password_hash(password)

	def check_password_hash(self,password):
		return check_password_hash(self.password,password)

	def getIdentifiers(self):
		return { 'username' : self.username, 'email' : self.email, 'role':self.role,
					'ranking' : self.ranking, 'rank_value' : self.rank_value
				}

	def getStats(self):
		return {  'total_submissions' : self.total_submissions, 'accepted' : self.accepted, 
					'wrong_answer' : self.wrong_answer, 'tle' : self.tle,				
				}

	def __repr__(self):
		return "<User { 'username' : %s,  'uid' : %s, 'role' : %s, 'submissions' : %d } >" % (self.username, self.uid, self.role, self.total_submissions)


# Every problem submission will be of this type
class Submission(db.Model):
	__tablename__ = 'submissions'
	
	# search using these values
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	uid = db.Column(db.String(255), nullable = False)
	submission_timestamp = db.Column(db.String(255),nullable=False)
	
	# basic info about the submission
	status = db.Column(db.String(50), nullable = False)
	user_id = db.Column(db.String(255), nullable = False)
	problem_id = db.Column(db.String(255), nullable = False)
	submission_language = db.Column(db.String(40), nullable = False)
	submission_location = db.Column(db.String(255),nullable = False)

	def __init__(self,status,user_uid,problem_uid,submission_language,location):
		self.status = status
		self.user_id = user_uid
		self.problem_id = problem_uid
		self.submission_language = submission_language
		self.submission_timestamp = datetime.datetime.today().isoformat(' ')
		self.uid = hashlib.sha1(self.submission_timestamp).hexdigest()
		self.submission_location=location

	def __repr__(self):
		return "<Submission { 'user_id' : %d, 'problem_id' : %d,  'lang' : %s,  'time' : %s } >" % (self.user_id,self.problem_id,self.submission_language,self.submission_timestamp)
	
	def getIdentifiers(self):
		return { 'user_id' : self.user_id, 'problem_id' : self.problem_id,}

	def getStats(self):
		return {  'status' : self.status,'lang':self.submission_language,}

	def getTimeStamp(self):
		return datetime.datetime.strptime(self.submission_timestamp, "%Y-%m-%d %H:%M:%S.%f")


# Every editorial comment will be of this type
class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	uid = db.Column(db.String(255), nullable = False, unique = True)
	comment_timestamp = db.Column(db.String(255), nullable = False)
	
	# basic info about the comment 
	user_id = db.Column(db.String(255), nullable = False)
	problem_id = db.Column(db.String(255), nullable = False)
	body = db.Column(db.String(400), nullable = False)

	def __init__(self, user_id, problem_id, body):
		self.user_id = user_id
		self.problem_id = problem_id
		self.body = body
		self.comment_timestamp = datetime.datetime.today().isoformat(' ')
		self.uid = hashlib.sha1(self.comment_timestamp).hexdigest()

	def __repr__(self):
		return "<Comment { 'uid' : %s, 'user_id' : %s, 'problem_id' : %s, 'comment_timestamp' : %s } >" % (self.uid, self.user_id, self.problem_id, self.comment_timestamp)

	def getStats(self):
		return {
					'user_id' : self.user_id,
					'problem_id' : self.problem_id,
					'comment_timestamp' : self.comment_timestamp
				}

	def getTimeStamp(self):
		return datetime.datetime.strptime(self.comment_timestamp, "%Y-%m-%d %H:%M:%S.%f")
