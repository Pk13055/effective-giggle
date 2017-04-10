# def imports required for routing etc
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, models
import config

# custom imports to handle files
import subprocess, os, shlex
import hashlib, random
import time, threading
import re

# title, tags, uploader, problem_location, self.io_location, solution_self.language, self.solution_location, editorial_location
# encapsulated body wherein you only have to create an object and call generate_result


class Solver():

	def __init__(self, language, solution_location, io_location, user_id, problem_id, timelimit):

		self.language = language
		self.solution_location = solution_location
		self.io_location = io_location
		self.user_id = user_id
		self.problem_id = problem_id
		self.timelimit = timelimit

	languages = { 	
		"C" : 'gcc', 
		"C++" : "g++", 
		"python 2" : "python 2.7",
		"python 3" : "python3", 
		"python 3.5" : "python3.5"
	}

	_result = {
		'user_id' : self.user_id,
		'problem_id' : self.problem_id,
		'submission_timestamp' : datetime.datetime.today().isoformat(' '),
		'submission_language' : self.language,
		'status' : [],
		'db_add' : False
	}

	# this function generates AND/OR runs the user code against the input file(s)
	def generate_result(self):
		
		try:
			# get JSON from this response
			test_cases = _generateLargeIO()
		except:
			return _result

		# compile and run if c, cpp or run directly
		sol_loc = os.path.join(config.UPLOAD_FOLDER_SUBMISSIONS, self.solution_location)
		# name buffer used for rapid io for large testcase
		test_buffer = hashlib.sha1(datetime.datetime.today().isoformat(':')).hexdigest() + '.txt'
		# location of the test buffer
		temp_loc = os.path.join(config.UPLOAD_FOLDER_SANDBOX, test_buffer)
		# location of the compile error file
		error_loc = os.path.join(config.UPLOAD_FOLDER_SANDBOX, self.user_id + test_buffer)
		
		# create a.out file first
		if self.language in ['C', 'C++']:
			# buffer file
			filename = hashlib.sha1(datetime.datetime.today().isoformat(':') + self.user_id).hexdigest()
			file_loc = os.path.join(config.UPLOAD_FOLDER_SANDBOX, filename)
			query = languages[self.language] + ' -w -std=c99 ' + sol_loc + ' -o ' + file_loc + ' -lm'
			e = open(error_loc, 'w')
			subprocess.call(shlex.split(query), stderr = e).wait()
			e.close()

			# if you have a compile error the _result status will be:
			# { 'status' : [ "Compile Error", "whatever error" ] }
			if os.path.getsize(error_loc):
				_result['status'].append("Compile Error")
				error = open(error_loc).read()
				_result['status'].append(error)
			else:
				run_query = file_loc
				for i, j in zip(test_cases['inputs'], test_cases['outputs']):
					open(temp_loc, 'w').write('\n'.join(i))
					inp = open(temp_loc)
					e = open(error_loc, 'w')
					try:
						op = subprocess.check_output(shlex.split(run_query), timeout = time, stderr = e, stdin = inp)
						e.close()
						# if os.path.getsize(error_loc):
						# 	_result['status'].append("Seg Fault")
						if op.decode('utf-8').strip('\n') == '\n'.join(j):
							_result['status'].append("Accepted")	
						else:
							_result['status'].append("Wrong Answer")
					except subprocess.CalledProcessError as error:
							_result['status'].append("Segmentation Fault (ERR_CODE %d)" % (error.returncode))
					except subprocess.TimeoutExpired:
							_result['status'].append("Timelimit exceeded")

		# run with python 
		elif self.language in ['python2', 'python3']:
			pass
		

		_result['added'] = createSubmission()
		return _result

	# this function gives us a list with the input, output strings 
	def _generateLargeIO(self):

		data = open(os.path.join(config.UPLOAD_FOLDER_TEST, self.io_location)).read().strip('\n').split('\n')
		# # comment out after done
		# data = open('testcase').read().strip('\n').split('\n')
		
		inputs = []
		outputs = []
		io_begs = [i for i, j in enumerate(data) if 'Input' in j]
		io_ends = [i for i, j in enumerate(data) if 'Output' in j]

		# in case input file is corrupt
		if len(io_begs) != len(io_ends):
			_result['status'].append("I/O Error")
			raise Exception
		
		else:
			# handle inputs
			for i, j in enumerate(io_begs):
				if i == len(io_begs) - 1:
					inputs.append(data[io_begs[i] + 1:io_ends[0]])
				else:
					inputs.append(data[io_begs[i] + 1: io_begs[i + 1]])
			# handle outputs
			for i, j in enumerate(io_ends):
				if i == len(io_ends) - 1:
					outputs.append(data[io_ends[i] + 1:len(data)])
				else:
					outputs.append(data[io_ends[i] + 1: io_ends[i + 1]])
			return {
				'inputs' : inputs,
				'outputs' : outputs
			}


	# this creates a submission object after processing and returns it if successful
	def createSubmission(self):
		try:
			db.session.add(models.Submission(','.join(_result['status']), _result['user_id'], _result['problem_id'], self.language, self.solution_location))
			db.session.commit()
			return True
		except:
			return False