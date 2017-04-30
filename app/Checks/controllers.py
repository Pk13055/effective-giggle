from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify

from app import db, models
import helper

check = Blueprint('check', __name__)


# this route is to maintain conformity with homepage nomenclature
@check.route('/checks', methods = ['GET'])
def checker():
	if request.method == 'GET':
		print(request.args['id'])
		if request.args['id'] == "user":
			message=helper.checkuser(request.args['value'])
		elif request.args['id'] == "email":
			message=helper.checkemail(request.args['value'])
		return jsonify(success=True,message=message)

	elif request.method == 'POST':
		pass
