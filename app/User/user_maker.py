# Methods to implement the various route validations and other helper

from flask import jsonify
from app import db, models
import app, config 

# modules to help across different functions
import os, hashlib, datetime
from werkzeug.utils import secure_filename


# Cross site function that checks if the uploaded file is valid
# specify the type1 as the set of file extensions to check for
def allowed_file(filename, type1):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in type1

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
			'profile_pic' : user.profile_location,
			'role':user.role,
			'uid':user.uid,
		}
		return user_data
	else:
		return {}

# Admin function to create a problem object from the submitted form
def createProblem(form, code, files):
	obj = {}
	for x in form:
		obj[x] = form[x]
	obj['uploader'] = code
	obj['files'] = files
	# obj contains all the data to build a problem and add to db
	# finally instead of returning, add the problem and then return 
	# title, tags, uploader, problem_location, io_location, solution_language, solution_location, editorial_location):
	return jsonify(obj)


# Admin function to upload the problem assoc files to the server - ADMIN ONLY 
def uploadFilesAdmin(files):
	exts = [config.ALLOWED_EXTENSIONS_PROBLEM, config.ALLOWED_EXTENSIONS_TEST, config.ALLOWED_EXTENSIONS_SOLUTION_CODE, config.ALLOWED_EXTENSIONS_EDITORIAL]
	locs = [config.UPLOAD_FOLDER_PROBLEM, config.UPLOAD_FOLDER_TEST, config.UPLOAD_FOLDER_SOLUTION_CODE, config.UPLOAD_FOLDER_EDITORIAL]
	final_paths = []
	for _ in range(4):
		file = files['file' + str(_)]
		if file and allowed_file(file.filename, exts[_]):
	            filename = hashlib.sha1(datetime.datetime.today().isoformat(':')).hexdigest() + '.' + file.filename.rsplit('.', 1)[1].lower()
	            final_paths.append(filename)
	            file.save(os.path.join(locs[_],final_paths[-1]))
	return final_paths

# get the problem data for the tables of admin page
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


# problems submitted for the user page
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
