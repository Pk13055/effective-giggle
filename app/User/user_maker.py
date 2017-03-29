# Methods to implement the various route validations and other helper

from flask import jsonify

def createProblem(form):
	obj = {}
	for x in form:
		if x == "tags" and len(form[x]):
			obj[x] = form[x].split(',')
		else:
			obj[x] = form[x]
	return jsonify(obj)