from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify
from app import db, models


comments = Blueprint('comments', __name__)


@comments.route('/comments/<code>', methods = ['GET', 'POST'])
def comments_render(code):
	if request.method == 'GET':
		return render_template('Main/comments.html', title = code)