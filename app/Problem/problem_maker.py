# Methods to implement the various route validations and other helper

from flask import jsonify
from app import db, models
import app

# modules to help across different functions
from werkzeug.utils import secure_filename
import os, config

# Admin function to upload the problem assoc files to the server
def userSubmission(file):
	# types = {'problem_text' : "", 'test_file' : "", 'problem_solution' : ""}
	# status = 1
	# for t in types:
	# 	if t not in files:
	# 		status = 0
	# 		break
	# return status
	try:
		if file:
			filename = secure_filename(file.filename)
			f = os.path.join(config.UPLOAD_FOLDER_SUBMISSION, filename)
			file.save(f)
		else:
			raise Exception
	except:
		return False

def getData(code):
	#for testing purpose 
	problems = models.Problem.query.all()
	# problem=problems[0]
	problem=problems[1]

	# problem = models.Problem.query.filter(models.Problem.uid == code).first()

	tag=problem.tags.split(',')

	file=open(config.BASE_DIR+"/problem_questions/load.txt","r")
	io_file=open(config.BASE_DIR+"/large_testcase/io.txt","r")
	io=io_file.read().split("\n")
	if problem:
		problem_data = {
			'id':problem.id,
			'uid':problem.uid,
			'title' : problem.title,
			'tags' : tag,		
			'problem':file.read(),
			'io':io,
		}
		return problem_data
	else:
		return {}
