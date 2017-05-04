from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify

from app import db, models
from app.models import User
import app,config
import problem_maker 
import os, hashlib, datetime
from werkzeug.utils import secure_filename
from app.Solver.solver_api import Solver
from app.User.user_maker import updateUser

problem = Blueprint('problem', __name__)

@problem.route('/problems/<code>', methods = ['GET', 'POST'])
def problem_render(code):
	
	if request.method == 'GET':
		problem = problem_maker.getData(code)
		return render_template('Main/problems.html.j2', problem = problem)			
	
	elif request.method == 'POST':
		if 'user_uid' not in session:
			return jsonify(success=False,redirect="/signin",message="you are not logged in")

		# saving the user submission on the server 		
		filename=problem_maker.createFile(request)
		if filename is None:
			return jsonify(success=False,message='Wrong File')			

		# generator api
		locations = problem_maker.getLocation(code) 

		#checking the user solution and giving saving the status
		solver =Solver(request.form['language'],filename,locations['io_location'],session['user_uid'],code,1.0)		
		result=solver.generate_result()

		# updating ranking and other user stats
		verdict=updateUser(result['status'],session['user_uid'])

		#updating the problem stats
		problem_maker.updateProblem(code,verdict)

		if result is not None:
			# print(result)
			return redirect('/solver/'+session['user_uid'])
		else:
			return jsonify(success=True,message="Something is wrong")
