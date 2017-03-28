from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, models


home = Blueprint('home', __name__)

@home.route('/', methods = ['POST', 'GET'])
def home_render():
	if request.method == 'GET':
		return render_template('Main/home.html')

@home.route('/signin', methods = ['POST', 'GET'])
def signin():
	if request.method == 'GET':
		return render_template('Forms/loginpage.html')

@home.route('/signup', methods = ['POST', 'GET'])
def signup():
	if request.method == 'GET':
		return render_template('Forms/registration.html')
