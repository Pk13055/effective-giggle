from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, models


problem = Blueprint('problem', __name__)

@problem.route('/problems/<code>', methods = ['GET', 'POST'])
def problem_render(code):
	if request.method == 'GET':
		return render_template('Main/problems.html', title = code)
