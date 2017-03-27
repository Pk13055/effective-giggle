import sys
from flask import Flask, render_template, jsonify
app = Flask(__name__, static_url_path='/static')

def main():
	port = 8000
	try:
		port = int(sys.argv[1])
	except:
		port = 8000
	app.run(debug = True, host = '127.0.0.1', port = port)



@app.errorhandler(404)
def page_exist(e):
	return render_template('error.html', error = e), 404

@app.route('/')
def home():
	return render_template('Main/home.html')


@app.route('/profile/<role>')
def profile(role):
	if role == "user":
		return render_template('Profiles/profile_user.html')
	else:
		return render_template('Profiles/profile_admin.html')

@app.route('/signup')
def signup():
	return render_template('Forms/registration.html')

@app.route('/signin')
def login():
	return render_template('Forms/loginpage.html')

@app.route('/problems/<code>')
def problem(code):
	return render_template('Main/problems.html', title = code)


@app.route('/comments/<code>')
def comments(code):
	return render_template('Main/comments.html', title = code)
if __name__ == '__main__':
	main()