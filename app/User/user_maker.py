# Methods to implement the various route validations and other helper

from flask import jsonify
from app import db, models
import app, config 

from app.models import Submission

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
			'profile_pic' : os.path.join('images', 'profile_pics', user.profile_location),
			'role':user.role,
			'uid':user.uid,
			'ranking':user.ranking,
			'rank_value':user.rank_value
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
	# text testcase solutione editorial
	# return jsonify(obj)
	try:
		db.session.add(models.Problem(obj['title'], obj['tags'], obj['uploader'], obj['files'][0], obj['files'][1], obj['solution_language'], obj['files'][2], obj['files'][3]))
		db.session.commit()
		return obj
	except:
		return None


# Admin function to upload the problem assoc files to the server - ADMIN ONLY 
def uploadFilesAdmin(files):
	exts = [config.ALLOWED_EXTENSIONS_PROBLEM, config.ALLOWED_EXTENSIONS_TEST, config.ALLOWED_EXTENSIONS_TEST, config.ALLOWED_EXTENSIONS_SOLUTION_CODE, config.ALLOWED_EXTENSIONS_EDITORIAL]
	locs = [config.UPLOAD_FOLDER_PROBLEM, config.UPLOAD_FOLDER_TEST, config.UPLOAD_FOLDER_TEST, config.UPLOAD_FOLDER_SOLUTION_CODE, config.UPLOAD_FOLDER_EDITORIAL]
	final_paths = []
	for _ in range(5):
		file = files['file' + str(_)]
		if file and allowed_file(file.filename, exts[_]):
				filename = hashlib.sha1(datetime.datetime.today().isoformat(':')).hexdigest() + '.' + file.filename.rsplit('.', 1)[1].lower()
				file.save(os.path.join(locs[_],filename))
				final_paths.append(filename)
				if _ == 2:
					ios = open(os.path.join(config.UPLOAD_FOLDER_TEST, final_paths[-2]), 'a+')
					ios.write(open(os.path.join(config.UPLOAD_FOLDER_TEST, filename)).read())
					ios.close()
					os.remove(os.path.join(config.UPLOAD_FOLDER_TEST, filename))
					final_paths = final_paths[:-1]
	return final_paths

# get the problem data for the tables of admin page
def getProblems(code):
	problems = models.Problem.query.filter(models.Problem.uploader == code).order_by(models.Problem.id.desc()).all()
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
	problems=models.Submission.query.filter(models.Submission.user_id == code).all()
	problem_list=[]
	for problem in problems:
		problem_name = models.Problem.query.filter(models.Problem.uid == problem.problem_id).with_entities(models.Problem.title).first().title
		status=problem.status.split(',')
		i=0
		
		while i < len(status):
			if(status[i] != "Accepted"):
				verdict=status[i]
				break;
			i=i+1	

		if i == len(status):
			verdict="Accepted"

		problem_list.append({
			'sub_uid':problem.uid,
			'uid':problem.problem_id,
			'largeStatus':problem.status,
			'status':verdict,
			'name':problem_name,
			'time':problem.submission_timestamp,
			'lang':problem.submission_language,
			})
	return problem_list[::-1]


def getStats(code):
	user = models.User.query.filter(models.User.uid == code).first()
	if user:
		user_stat = {
		 "accepted":user.accepted,
		"tle":user.tle,
		"wrong_answer":user.wrong_answer,
		}
		return user_stat
	else:
		return {}

		
def updateUser(status,user_uid):
	user=models.User.query.filter(models.User.uid==user_uid).first()
	# print(user)

	i=0
	while i < len(status):
		if(status[i] != "Accepted"):
			verdict=status[i]
			break;
		i=i+1	

	if i == len(status):
		verdict="Accepted"		

	if verdict == "Accepted":
		user.rank_value=20+user.rank_value 	
	else:
		user.rank_value=user.rank_value-5

	if verdict == "Accepted":
		user.accepted=1 + user.accepted
	elif verdict == "Wrong Answer":
		user.wrong_answer=1 + user.wrong_answer
	elif verdict == "Timelimit exceeded":
		user.tle=1+user.tle

	if user.rank_value < 1000:
		user.ranking = "Lost"

	elif user.rank_value < 1500 :
		user.ranking = "Newbie"

	elif user.rank_value < 1700 :
		user.ranking ="Warrior"
	
	else:
		user.ranking ="Legend"

	user.total_submissions=1 + user.total_submissions

	db.session.commit()	
	return verdict

def getUserSubmission(uid):
	submission=models.Submission.query.filter(models.Submission.uid==uid).first()
	if submission is None :
		return "No such submission"
	else:
		return submission

def getSubFile(name):
	file = open(os.path.join(config.UPLOAD_FOLDER_SUBMISSION,name)).read()
	return file