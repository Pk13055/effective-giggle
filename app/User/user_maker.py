# Methods to implement the various route validations and other helper

from flask import jsonify
from app import db, models
import app

# modules to help across different functions
from werkzeug.utils import secure_filename
import os, config


# Cross site function that checks if the uploaded file is valid
def allowed_file(filename, type):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.type


# Admin function to upload the problem assoc files to the server
def uploadFiles(files, code):
	types = {'problem_text' : "", 'test_file' : "", 'problem_solution' : ""}
	status = 1
	for t in types:
		if t not in files:
			status = 0
			break
	return status
	try:
		if status:
			for _ in types:
				file = files[_]
				if file:
					filename = secure_filename(file.filename)
					if _ == 'problem_text':
						f = os.path.join(config.UPLOAD_PROBLEM, filename)
					elif _ == 'test_file':
						f = os.path.join(config.UPLOAD_TEST, filename)
					elif _ == 'problem_solution':
						f = os.path.join(config.UPLOAD_SOLUTION, filename)
					types[_] = f
					file.save(f)
				else:
					raise Exception
			return types
		else:
			return False
	except:
		return False


# Admin function to create a problem object from the submitted form
def createProblem(form, code, files):
	obj = {}
	for x in form:
		obj[x] = form[x]
	obj['uploader'] = code
	try:
		for x in files:
			obj[x] = files[x]
	except:
		pass
	return jsonify(obj)

# Admin function to render the dict data for the given admin
def getData(code):
	user = models.User.query.filter(models.User.uid == code).first()
	if user:
		user_data = {
			'username' : user.username,
			'email' : user.email,
			'location' : user.location,
			'institute' : user.institute,
			'uid' : code,
			'profile_pic' : user.profile_location
		}
		return user_data
	else:
		return {}

def getProblems(code):
	problems = models.Problem.query.filter(models.Problem.uploader == code).all()
	problem_list = []
	for problem in problems:
		problem_list.append({
				'title' : problem.title,
				'attempted' : problem.total_submissions,
				'accepted' : problem.accepted,
				'wrong_answer' : problem.wrong_answer,
				'tle' : problem.tle
			})
	return problem_list

def getProblemSubmitted(code):
	problems=models.Submission.query.filter(models.Submission.user_id==code).all()
	problem_list=[]
	for problem in problems:
		problem_name=models.Problem.query.filter(models.Problems.uid==problem.uid)
		problem_list.append({
			'status':problem.status,
			'name':problem_name,
			'time':problem.submission_timestamp,
			'lang':problem.submission_language,
			})
	return problem_list	
