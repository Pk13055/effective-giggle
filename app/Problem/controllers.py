from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify

from app import db, models
from app.models import User
import app,config
import problem_maker 
import os, hashlib, datetime
from werkzeug.utils import secure_filename
from app.Solver.solver_api import Solver


problem = Blueprint('problem', __name__)

@problem.route('/problems/<code>', methods = ['GET', 'POST'])
def problem_render(code):
	problem=problem_maker.getData(code)
	if request.method == 'GET':
		return render_template('Main/problems.html', problem = problem)			

	elif request.method == 'POST':
		if 'user_uid' not in session:
			return jsonify(success=False,redirect="/signin",message="you are not logged in")
		
		filename=problem_maker.createFile(request)
		if filename is None:
			return jsonify(success=False,message='Wrong File')			

		# generator api
		result=True
		if result is True:
			return jsonify(success=True,redirect="/solver/"+session['user_uid'])
		else:
			return jsonify(success=True,message="Something is wrong")
