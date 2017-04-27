# Methods to implement the various route validations and other helper

from flask import jsonify,session
from app import db, models, sanitize
import app

# modules to help across different functions
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import os,hashlib,config,datetime

# this function is responsible for rendering the problem page
# it returns a JSON with the required fields and if the file is not readable it returns an empty dataset
def getData(code):
	
	problem_data = models.Problem.query.filter(models.Problem.uid == code).first()
	filename = problem_data.problem_location
	tags = problem_data.tags.split(',')
	tags = sanitize(tags)
	
	return_obj = {
		'id':problem_data.id,
		'uid':problem_data.uid,
		'title' : problem_data.title,
		'tags' : tags,
		'status' : [],
		'heading' : [],
		'introduction' : [],
		'constraints' : [],
		'testcases' : []
	}
	# in case the problem does not exist or cannot be parsed
	data = ["This problem does not have a question"]
	
	try:
		data = open(os.path.join(config.UPLOAD_FOLDER_PROBLEM, filename)).read().strip('\n').split('\n')
		data = sanitize(data)
	except:
		pass
	
	if data:
		markers = []
		data_headers = ['Introduction', 'Heading', 'Constraints', 'Test Cases']
		for i, j in enumerate(data):
			if j.strip(' ') in data_headers:
				markers.append(i)
		if len(markers) != len(data_headers):
			return_obj['heading'] = data
		else:
			# this stores the final data as a LOFL
			dataset = []
			for i, j in enumerate(markers):
				try:
					dataset.append(data[markers[i] + 1: markers[i + 1]])
				except:
					dataset.append(data[markers[i] + 1:])
			fillers = ['heading', 'introduction', 'constraints', 'testcases']
			
			# this loop fills the given dataset values into the return object
			for i,j in enumerate(fillers):
				return_obj[j] = dataset[i]
			
			test_cases = []
			io_pos = [i for i, j in enumerate(return_obj['testcases']) if "Input" in j]
			for i, j in enumerate(io_pos):
				try:
					test_cases.append(return_obj['testcases'][j : io_pos[i + 1]])
				except:
					test_cases.append(return_obj['testcases'][j :])

			return_obj['testcases'] = test_cases
			return_obj['status'].append("Data Parsed")
	
	else:
		return_obj['status'] = data
	
	return return_obj


'''		
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
		il = []
		ol = []
		il.append(0)
		ol.append(0)
		n = len(lines)
		i = 0
		#print(lines[0])
		count = 0
		while i < n and count < 1000:
		#print("yo")
			count = count +1
			if lines[i] == 'Heading': 
				i += 2
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
				il.append(0)
				print(testcases)
				while lines[i] != 'Output':
					inputs.append(lines[i])
					i += 1
					il[testcases] += 1
			if lines[i] == 'Output':
				i += 1
				ol.append(0)
				while (i < n and lines[i] != 'Input'):
					outputs.append(lines[i])
					i += 1
					ol[testcases] += 1
		maxlen = max(il) + max(ol)			
			 	
	
	except:
	 	introduction = 'you dont need question to solve this problem'
	 	constraints = []
	 	inputs = []
	 	outputs = []
	 	testcases = 0
	 	il = []
	 	ol = []
	 	maxlen = 0
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
			'maxlen' : maxlen,
		}
		return problem_data
	else:
		return {}
'''

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

	# print(problem.wrong_answer)

	db.session.commit()
