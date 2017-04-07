# define the functions to be used alongside routes here
# This modular design will help the routes from becoming too cluttered

from flask import jsonify
from app.models import Comment, User
from app import db, models
import config

# custom imports 
import os

# this function adds the comment to the db 
def addComment(form, code):
	user_id = form['user_id']
	text = form['body']
	try:
		if user_id == "":
			raise Exception
		else:
			db.session.add(Comment(user_id, code, text))
			db.session.commit()
		return True
	except:
		return None


# this gets you the comments in the form of a JSON-esque object
# each member contains the name, profile_pic, timestamp, body
def getComments(code):
	comments = Comment.query.join(User, User.uid == Comment.user_id).add_columns(User.username, User.profile_location, Comment.comment_timestamp, Comment.body).filter(Comment.problem_id == code).order_by(Comment.id.desc()).all()
	comment_list = []
	for comment in comments:
		comment_list.append({
				'name' : comment.username,
				'profile_pic' : comment.profile_location,
				'timestamp' : comment.comment_timestamp[:-7],
				'body' : comment.body
			})
	return comment_list

# this gets you the title of the problem and the editorial location
# modify to make editorial support markdown as well
def getData(code):
	data = models.Problem.query.filter(models.Problem.uid == code).with_entities(models.Problem.title, models.Problem.editorial_location).first()
	try:
		body = open(os.path.join(config.UPLOAD_FOLDER_EDITORIAL, data.editorial_location)).read()
		body = getMarkdown(body,data.editorial_location)
		file_ext= data.editorial_location.rsplit('.',1).lower()
		# file = request.files['file0']
		# filename = data.editorial_location
		
	except:
		body = "No Editorial available for this problem"
		file_ext = "txt"
	return {'title' : code, 'editorial_location' : body, 'check':file_ext}


def getMarkdown(body,filename):
	file_ext= data.editorial_location.rsplit('.',1).lower()
	if body and '.' in data.editorial_location and data.editorial_location.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS_EDITORIAL:
		if(file_ext=='txt'):
			body=markdown.markdown(body)
			return body
		else:
			return body