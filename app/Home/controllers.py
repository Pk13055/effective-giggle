from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify

from app import db, models,requires_auth 
import helper

home = Blueprint('home', __name__)


# this route is to maintain conformity with homepage nomenclature
@home.route('/', methods = ['GET'])
def homie():
	return redirect(url_for('home.home_render', page = 1))

# this route renders the main page of the website
@home.route('/<page>', methods = ['POST', 'GET'])
def home_render(page):
	if request.method == 'GET':
		data = helper.makeHome(page)
		return render_template('Main/home.html', latest_problems = data['latest'], current_page = data['current'], total_pages = data['total'])
		# return jsonify(helper.makeHome(page))
	elif request.method == 'POST':
		# add the search functionality here
		pass


# this route is for signing into the website
@home.route('/signin', methods = ['POST','GET'])
def signin():
	if request.method == 'GET':
		return render_template('Forms/loginpage.html')
	elif request.method == 'POST':
		try:
			email = request.form['email']
			password = request.form['password']
		except KeyError as e:
			return jsonify(success = False, message = " %s doesnt exist") % e.args, 400
		user = models.User.query.filter(models.User.email == email).first()
		if user is None:
			return jsonify(success = False, message = "Register First"), 401
		elif not user.check_password_hash(password):
			return jsonify(success = False, message = "Wrong Password"), 401
		session['user_uid'] = user.uid
		return jsonify(redirect = '/solver/' + user.uid)

# simple logout route
@home.route('/logout',methods = ['POST','GET'])
@requires_auth
def logout():
	session.pop('user_uid')
	return redirect('/signin')
			

# route for signing up 
@home.route('/signup', methods = ['POST', 'GET'])
def signup():
	if request.method == 'GET':
		return render_template('Forms/registration.html')
	elif request.method == 'POST':
		result = helper.createmodels.User(request)
		if result is True:
			return render_template('Forms/loginpage.html')
		else:
			return result
