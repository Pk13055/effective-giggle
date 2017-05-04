from flask import Blueprint, request, render_template, \
				  flash, g, session, redirect, url_for, jsonify
from app import db, requires_auth
from app.models import User
import user_maker


user = Blueprint('user', __name__)

@user.route('/setter/<code>', methods = ['GET', 'POST'])
@requires_auth
def admin_route(code):
	if request.method == 'GET':
		data = user_maker.getData(code)
		if data:
			problems = user_maker.getProblems(code)
			return render_template('Profiles/profile_admin.html.j2', admin = code, data = data, problems = problems)
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
		stats=user_maker.getStats(code)
		problems_submitted = user_maker.getProblemSubmitted(code)
		if data:
			return render_template('Profiles/profile_user.html.j2',data = data,problems = problems_submitted,stats=stats)
		else:
			return render_template('error.html.j2',error="View did not return response")	

@user.route('/solver/submission', methods = ['GET', 'POST'])
@requires_auth
def user_submission():
	if request.method == 'GET':
		data=user_maker.getUserSubmission(request.args['uid'])
		file=user_maker.getSubFile(data.submission_location)
		return render_template('Profiles/user_submission.html.j2',data=data,file=file)

@user.route('/userlist/<code>', methods = ['GET', 'POST'])
def userlist(code):
	if request.method == 'GET':
		data=user_maker.getUsers(code)
		length=User.query.count()
		return render_template('Profiles/userlist.html.j2',users = data,length=length)
