import sys
from flask import Flask, render_template, jsonify
app = Flask(__name__, static_url_path='/static')

def main():
	app.run(debug = True, host = '127.0.0.1', port = int(sys.argv[1]))


@app.route('/')
def home():
	return render_template('Main/home.html')

if __name__ == '__main__':
	main()