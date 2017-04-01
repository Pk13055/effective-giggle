from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, models

import user_maker


user = Blueprint('user', __name__)

@user.route('/setter/<code>', methods = ['GET', 'POST'])
# 6da345d3e597b17c5a6e32b011dcb823c1fca8ef use this guy for testing
def admin_route(code):
	if request.method == 'GET':
		data = user_maker.getData(code)
		if data:
			problems = user_maker.getProblems(code)
			return render_template('Profiles/profile_admin.html', admin = code, data = data, problems = problems)
		else:
			redirect("/", code = 404)
	elif request.method == 'POST':
		return user_maker.createProblem(request.form, code)


@user.route('/solver/<code>', methods = ['GET', 'POST'])
def user_route(code):
	if request.method == 'GET':
		return render_template('Profiles/profile_user.html')
