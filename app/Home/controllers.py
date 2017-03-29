from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, models
import helper

home = Blueprint('home', __name__)

@home.route('/', methods = ['POST', 'GET'])
def home_render():
	if request.method == 'GET':
		return render_template('Main/home.html')

@home.route('/signin', methods = ['POST', 'GET'])
def signin():
	if request.method == 'GET':
		return render_template('Forms/loginpage.html')
	elif request.method == 'POST':
		return helper.makeJSON(request.form['email'], request.form['username'], request.form['password'])

@home.route('/signup', methods = ['POST', 'GET'])
def signup():
	if request.method == 'GET':
		return render_template('Forms/registration.html')
	elif request.method == 'POST':
		return helper.makeNewUser(request.form)
