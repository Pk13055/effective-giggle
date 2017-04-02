from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, models

import problem_maker 

problem = Blueprint('problem', __name__)

@problem.route('/problems/<code>', methods = ['GET', 'POST'])
def problem_render(code):
	if request.method == 'GET':
		problem=problem_maker.getData(code)
		return render_template('Main/problems.html', problem = problem)
	elif request.method == 'POST':
		# file=problem_maker.userSubmission(request.files)
		return jsonify(redirect='/solver/'+session['user_uid'])
		