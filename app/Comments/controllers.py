
# def imports required for routing etc
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, models
import helper


comments = Blueprint('comments', __name__)


@comments.route('/comments/<code>', methods = ['GET', 'POST'])
def comments_render(code):
	try:
		user_id = session['user_uid']
	except:
		user_id = ""
	if request.method == 'GET':
		comment_obj = helper.getComments(code)
		title = helper.getData(code)
		return render_template('Main/comments.html', title = title['title'], comments = comment_obj, editorial = title['editorial_location'], code = code, user_id = user_id,check=title['check'])
		# return jsonify(comment_obj)
	elif request.method == 'POST':
		helper.addComment(request.form, code)
		return redirect(url_for('comments.comments_render', code = code))
