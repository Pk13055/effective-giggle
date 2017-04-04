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
	
	# problems = models.Problem.query.all()
	# problem=problems[0]
	# problem=problems[1]

	problem = models.Problem.query.filter(models.Problem.uid == code).first()

	try:
		tag=problem.tags.split(',')
	except:
		tag="None"

	# returns the data from each location
	try:
		file=open(config.BASE_DIR+problem_location,"r").read()
	except:
		file="You dont need the question to answer this"
	try:
		io_file=open(config.UPLOAD_FOLDER_SUBMISSION+io_location,"r")
		io=io_file.read().split("\n")
	except:
		io=str("--")

	if problem:
		problem_data = {
			'id':problem.id,
			'uid':problem.uid,
			'title' : problem.title,
			'tags' : tag,		
			'problem':file,
			'io':io,
		}
		return problem_data
	else:
		return {}

def allowed_file(filename, type1):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in type1

def uploadFileUser(file):
	exts = config.ALLOWED_EXTENSIONS_CODE
	locs = config.UPLOAD_FOLDER_SUBMISSION
	if file and allowed_file(file.filename, exts):
		filename = hashlib.sha1(datetime.datetime.today().isoformat(':')).hexdigest() + '.' + file.filename.rsplit('.', 1)[1].lower()
		file.save(os.path.join(locs,file.filename))
	else:
		return "Not allowed"

	return filename

def Submit(form,problem_uid,file):
	obj = {}
	# for x in form:
	# 	obj[x]=form[x]
	obj['file']=file
	file_location=config.UPLOAD_FOLDER_SUBMISSION+file

	print(obj)
	try:
		sub=models.Submission("Queued",obj['user_uid'],problem_uid,obj['language'],file_location)
		print(sub)
		db.session.add(sub)
		db.session.commit()
		return obj
	except:
		return "Not Added to the database"
		