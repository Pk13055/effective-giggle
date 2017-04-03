import os
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify

from app import db, models,requires_auth 
import helper

home = Blueprint('home', __name__)

@home.route('/', methods = ['POST', 'GET'])
def home_render():
	if request.method == 'GET':
		return render_template('Main/home.html')

@home.route('/signin', methods = ['POST','GET'])
def signin():
	if request.method == 'GET':
		return render_template('Forms/loginpage.html')
	elif request.method == 'POST':
		return helper.signInUser(request)


@home.route('/logout',methods = ['POST','GET'])
@requires_auth
def logout():
	session.pop('user_uid')
	return redirect('/signin')
			
@home.route('/signup', methods = ['POST', 'GET'])
def signup():
	if request.method == 'GET':
		return render_template('Forms/registration.html')
	elif request.method == 'POST':
		return helper.createUser(request)
