# Methods to implement the various route validations and other helper

from flask import jsonify,session
from app import db, models
import app

# modules to help across different functions
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import os,hashlib,config,datetime

def getData(code):
	#for testing purpose 
	
	# problems = models.Problem.query.all()
	# problem=problems[0]
	# problem=problems[1]
	problem = models.Problem.query.filter(models.Problem.uid == code).first()
	problem_location = problem.problem_location
	try:
		tag=problem.tags.split(',')
	except:
		tag="None"

	# returns the data from each location
	try:
	# open(config.BASE_DIR+problem_location,"r").read()
		lines = open(os.path.join(config.UPLOAD_FOLDER_PROBLEM, problem_location)).read().strip('\n').split('\n')
		introduction = ""
		constraints = []
		testcases = 0
		inputs = []
		outputs = []
		n = len(lines)
		i = 0
		#print(lines[0])
		while i < n:
			#print("yo")
			if lines[i] == 'Heading': 
				i += 1
			if lines[i] == 'Introduction':
				i += 1
				while lines[i] != 'Constraints':
					introduction = introduction + lines[i] + "\n"
					i += 1			
			if lines[i] == 'Constraints':
				i += 1
				while lines[i] != 'Test Cases':
					constraints.append(lines[i]) 
					i += 1
			if lines[i] == 'Test Cases':
				i+=1
			if lines[i] == 'Input':
				i += 1
				testcases += 1
				while lines[i] != "Output":
					inputs.append(lines[i])
					i += 1
			if lines[i] == 'Output':
				i += 1
				while (i < n and lines[i] != 'Input'):	
					outputs.append(lines[i])
					i += 1
		il = len(inputs)/testcases
		ol = len(outputs)/testcases	 	
	
	except:
	 	introduction = 'you dont need question to solve this problem'
	 	constraints = []
	 	inputs = []
	 	outputs = []
	 	testcases = 0
	 	il = 0
	 	ol = 0
	try:
		io_file=open(config.UPLOAD_FOLDER_TEST+
			"/"+problem.io_location,"r")
		io=io_file.read().split("\n")
	except:
		io=str("--")

	if problem:
		problem_data = {
			'id':problem.id,
			'uid':problem.uid,
			'title' : problem.title,
			'tags' : tag,		
			'problem':introduction,
			'io':io,
			'constraints' :constraints,
			'inputs' : inputs,
			'outputs' : outputs,
			'testcases' : testcases,
			'inputlength' : il,
			'outputlength' : ol,
		}
		return problem_data
	else:
		return {}

def getLocation(code):
	problem = models.Problem.query.filter(models.Problem.uid == code).first()
	locations={}
	locations['io_location']=problem.io_location
	locations['problem_location']=problem.problem_location
	return locations

def createFile(request):
	file=request.files['file007']
	filename=file.filename
	if file and '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS_CODE:
		filename = hashlib.sha1(session['user_uid']+datetime.datetime.today().isoformat(':')).hexdigest() + '.' + filename.rsplit('.', 1)[1].lower()
		file.save(os.path.join(config.UPLOAD_FOLDER_SUBMISSION, filename))
		return filename		
	else: 
		return None   

def updateProblem(problem_uid,verdict):
	problem = models.Problem.query.filter(models.Problem.uid == problem_uid).first()

	if verdict == "Accepted":
		problem.accepted=1 +problem.accepted
	elif verdict == "Wrong Answer":
		problem.wrong_answer=1 + problem.wrong_answer
	elif verdict == "Timelimit exceeded":
		problem.tle=1+problem.tle

	problem.total_submissions=1 + problem.total_submissions 	

	print(problem.wrong_answer)

	db.session.commit()
