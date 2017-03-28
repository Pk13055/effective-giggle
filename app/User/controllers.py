from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, models


user = Blueprint('user', __name__)

@user.route('/setter/<code>', methods = ['GET', 'POST'])
def admin_route(code):
	if request.method == 'GET':
		return render_template('Profiles/profile_admin.html')

@user.route('/solver/<code>', methods = ['GET', 'POST'])
def user_route(code):
	if request.method == 'GET':
		return render_template('Profiles/profile_user.html')
