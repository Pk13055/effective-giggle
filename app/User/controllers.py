from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, requires_auth

import user_maker


user = Blueprint('user', __name__)

@user.route('/setter/<code>', methods = ['GET', 'POST'])
def admin_route(code):
	if request.method == 'GET':
		data = user_maker.getData(code)
		if data:
			problems = user_maker.getProblems(code)
			return render_template('Profiles/profile_admin.html', admin = code, data = data, problems = problems)
		else:
			redirect("/", code = 404)
	elif request.method == 'POST':
		filenames = user_maker.uploadFilesAdmin(request.files)
		user_maker.createProblem(request.form, code, filenames)
		return redirect(url_for('user.admin_route', code = code))


@user.route('/solver/<code>', methods = ['GET', 'POST'])
@requires_auth
def user_route(code):
	if request.method == 'GET':
		data=user_maker.getData(code)
		#use this to test jinja page 
		# problems_submitted=[{'status':"Wrong Answer",'name':'42','time':'1/2/12','lang':'C++'},{'status':"Accepted",'name':'Graph','time':'12/21/12','lang':'Python'}]
		problems_submitted = user_maker.getProblemSubmitted(code)
		return render_template('Profiles/profile_user.html',data = data,problems = problems_submitted)
