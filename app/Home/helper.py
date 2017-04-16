# This file will contain all the functions associated 
# with the routes in the Home folder, so as to keep routing as minimal as possible
from app import db, models
from flask import jsonify
import config


# helper modules required
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from app.models import User
import os, hashlib, datetime
from app.models import Problem


# makes a JSON response, use this function for testing purpose
def makeJSON(email, username, password):
		role = "admin"
		if email:
			auth_id = email
			auth_type = "email"
		else:
			auth_id = username
			auth_type = "username"
		return jsonify({'auth_id' : auth_id, 'auth_type' : auth_type, 'password' : password, 'role' : role})


# collects data from the user form and returns a new user
def makeNewUser(form):
	obj = {}
	for x in form:
		if x != 'submit' and x != 'password_2':
			obj[x] = form[x]
	return jsonify(obj)

# creates and adds the user to the db
def createUser(request):
	try:
		email = request.form["email"]
		institute = request.form["institute"]
		location = request.form["location"]
		password = request.form["password"]
		role = request.form["role"]
		username = request.form["username"]
		
		file = request.files['file0']
		filename = file.filename
		
		if file and '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS_IMAGE:
			filename = hashlib.sha1(datetime.datetime.today().isoformat(':')).hexdigest() + '.' + filename.rsplit('.', 1)[1].lower()
			file.save(os.path.join(config.UPLOAD_FOLDER_IMAGE, filename))
			profile_location = filename
		else:
			profile_location = config.STANDARD_IMAGE

	except KeyError as e:
		return jsonify(success=False, message="%s not sent in the request" % e.args), 400 

	u = User(username, email, password, institute, location, role, profile_location)
	db.session.add(u)
	try:
		db.session.commit()
	except IntegrityError as e:
		return jsonify(success=False, message="This email already exists"), 400		
	return True


# change these two params to have the number of problems per page change
LATEST = 6
PER_PAGE = 6


data = {
	'latest' : [],
	'current' : [],
	# 'total' : len(PROBLEMS)/PER_PAGE 
}

def makeData(begin, end, key, PROBLEMS):
	data[key] = []
	for i in range(begin, end):
		
		try:
			abstract = open(os.path.join(config.UPLOAD_FOLDER_EDITORIAL, PROBLEMS[i].editorial_location)).read(50)
		except:
			abstract = "Click attempt to read more!"
		try:
			if PROBLEMS[i].tags == "":
				tags = []
			else:
				tags = PROBLEMS[i].tags.split(',')[:4]
		except:
			break
		data[key].append({
			'uid' : PROBLEMS[i].uid,
			'id' : PROBLEMS[i].id,
			'title' : PROBLEMS[i].title,
			'tags' : tags,
			'abstract' : abstract
		})
	data['total'] = len(PROBLEMS)/PER_PAGE

def makeHome(page):
	PROBLEMS = models.Problem.query.with_entities(models.Problem.uid, models.Problem.title, models.Problem.id, models.Problem.tags, models.Problem.editorial_location).order_by(models.Problem.id.desc()).all()
	makeData(0, LATEST, 'latest', PROBLEMS)
	current_beg = LATEST + (int(page) - 1)*PER_PAGE
 	current_end = min(current_beg + PER_PAGE,db.session.query(models.Problem).count()) 
	makeData(current_beg, current_end, 'current', PROBLEMS)
	return data


# def search_list(val,key):
def search_list(value,key):

	val=value.split(' ')

	problem_list=[]
	problem_list_opt=[]
	# by tag
	for tag in val:
		problems=Problem.query.filter(Problem.tags.like("%"+tag+"%")).all()		 
		print(problems)
		for problem in problems:
			dict1={}
			dict1['id']=problem.id
			dict1['title']=problem.title
			dict1['uid']=problem.uid
			dict1['tags']=problem.tags.split(',')
			problem_list.append(dict1)

	# by name
	for value in val:
		problems=Problem.query.filter(Problem.title.like("%"+value+"%")).all()		 

		for problem in problems:
			dict1={}
			dict1['id']=problem.id
			dict1['title']=problem.title
			dict1['uid']=problem.uid
			dict1['tags']=problem.tags.split(',')
			problem_list.append(dict1)

	# problem_list.sort(key = lambda x : x['title'])

	# by code
	for code in val:
		problems=Problem.query.filter(Problem.id.like("%"+code+"%")).all()		 
		for problem in problems:
			dict1={}
			dict1['id']=problem.id
			dict1['title']=problem.title
			dict1['uid']=problem.uid
			dict1['tags']=problem.tags.split(',')
			problem_list.append(dict1)
	
	ran=int(key)*10 - 1 

	problem_list_opt=[]
	for x in range(ran-10,ran) :
		try:
			problem_list_opt.append(problem_list[x])
		except:
			break


	dict1={}
	dict1['list']=problem_list_opt
	dict1['total_pages']=len(problem_list)/10 +1
	dict1['current_page']=key
	# print(dict1)
	return dict1
	# return problem_list


