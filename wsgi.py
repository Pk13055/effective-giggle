import sys
from flask import Flask, render_template, jsonify
from app import app as application

def main():
	port = 5000
	try:
		port = int(sys.argv[1])
	except:
		pass
<<<<<<< HEAD
	application.run(debug = True, host = '0.0.0.0', port = port)
=======
	application.run(debug = True, host = '127.0.0.1', port = port)
>>>>>>> f7ba06c439095d70774a611af5a89e27f663da13

if __name__ == '__main__':
	main()	
