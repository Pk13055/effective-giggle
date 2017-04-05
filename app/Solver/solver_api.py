# def imports required for routing etc
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, models
import config

# custom imports to handle files
import subprocess, os
import hashlib, random
import time, threading
import re

# by current implementation, admin code is just for backup purpose and is never used
# title, tags, uploader, problem_location, io_location, solution_language, solution_location, editorial_location

problem_file = "somehash.c"
large_testcase = io_location
solution_language = "C"
solution_file = "some hash"

languages = { 	
				"C" : 'gcc', 
				"C++" : "g++", 
				"python 2.7" : "python 2.7",
				"python 3" : "python3", 
				"python 3.5" : "python3.5"
			}

result = {
	'user_id' : user_id,
	'problem_id' : problem_id,
	'submission_timestamp' : datetime.datetime.today().isoformat(' '),
	'submission_language' : language,
	'status' : []
}

# this function generates AND/OR runs the user code against the input file(s)
def generateResult(language, solution_location, io_location, user_id, problem_id):
	test_cases = generateLargeIO(io_location)
	sol_loc = os.path.join(config.UPLOAD_FOLDER_SUBMISSIONS, solution_location)
	test_buffer = hashlib.sha1(datetime.datetime.today().isoformat(':')).hexdigest() + '.txt'
	temp_loc = os.path.join(config.UPLOAD_FOLDER_SANDBOX, test_buffer)
	# create a.out file first
	if language in ['C', 'C++']:
		filename = hashlib.sha1(datetime.datetime.today().isoformat(':') + user_id).hexdigest()
		pass
	# run with python 
	else:
		pass
	return result

# this function gives us a list with the input strings 
def generateLargeIO(io_location):
	data = open(os.path.join(config.UPLOAD_FOLDER_TEST, io_location)).read().split('\n')
	inputs = []
	outputs = []
	test_cases = []
	io_begs = [i for i, j in enumerate(data) if 'Input' in j]
	io_ends = [i for i, j in enumerate(data) if 'Output' in j]
	for beg, end in zip(io_begs, io_ends):
		inputs.append(data[beg + 1: end])
	return [ '\n'.join(_) for _ in inputs]

def createSubmission(result):
	try:
		db.session.add(models.Submission(result['submission_timestamp'], result['status'], result['user_id'], result['problem_id']))
		db.session.commit()
		return result
	except:
		return None