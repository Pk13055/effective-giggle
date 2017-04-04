from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify

from app import db, models
from app.models import User
import app,config
import problem_maker 
import os, hashlib, datetime
from werkzeug.utils import secure_filename

problem = Blueprint('problem', __name__)

@problem.route('/problems/<code>', methods = ['GET', 'POST'])
def problem_render(code):
	if request.method == 'GET':
		problem=problem_maker.getData(code)
		if 'user_uid' in session:
			user=session['user_uid']
			return render_template('Main/problems.html', problem = problem,user_uid=user)
		else:
			return render_template('Main/problems.html', problem = problem)			

	elif request.method == 'POST'	:
		# filename = problem_maker.uploadFileUser(request.form['file'])
		# return jsonify(sucess=False,file=code)
		print(request.form)
		problem_maker.Submit(request.form,code,"filename")
		try:
			return jsonify(redirect='/solver/'+request.form['user_uid'])
		except:
			return jsonify(sucess=False,message="Something went wrong")
