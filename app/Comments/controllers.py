from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, models
from helper import *

from selenium import webdriver
import urllib
import urllib2

comments = Blueprint('comments', __name__)


@comments.route('/comments/<code>', methods = ['GET', 'POST'])
def comments_render(code):
	if request.method == 'GET':
		comments = models.Comment.query.filter(models.Comment.problem_id == code).with_entities(Comment.user_id).all()
		comment_obj = []
		for comment in comments:
			user = models.User.filter(User.uid == comment.user_id).all()
			user = user[0]
			comment_obj.append({ 'name' : user.username, 'profile_pic' : user.profile_pic, 
				'timestamp' : comment.comment_timestamp, 'body' : comment.body })
		driver = webdriver.Firefox()
		driver.get(driver.getCurrentUrl())
		logged_in = 34
		return render_template('Main/comments.html', title = code, comments = comment_obj, user_id = logged_in)
	elif request.method == 'POST':
		addStudent(request.form, code)
		redirect('/comments/' + str(code))
