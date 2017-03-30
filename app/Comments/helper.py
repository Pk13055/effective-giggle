# define the functions to be used alongside routes here
# This modular design will help the routes from becoming too cluttered

from app.models import Comment
from app import db

def addComment(form, problem_id):
	user_id = form['user_id']
	text = form['body']
	try:
		db.session.add(Comment(user_id, problem_id, text))
		db.session.commit()
	except:
		return False