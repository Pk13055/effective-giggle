# Methods to implement the various route validations and other helper

from flask import jsonify
from app import db, models

# Admin function to create a problem object from the submitted form
def createProblem(form, code):
	obj = {}
	for x in form:
		obj[x] = form[x]
	obj['uploader'] = code
	return jsonify(obj)

# Admin function to render the dict data for the given admin
def getData(code):
	user = models.User.query.filter(models.User.uid == code, models.User.role == 'admin').first()
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