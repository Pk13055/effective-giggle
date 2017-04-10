# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
UPLOAD_BASE = os.path.abspath(os.path.join(BASE_DIR, 'uploads'))
STANDARD_IMAGE = 'kitten.jpeg'

# Defining the upload criterion for the various files uploaded by the user

# dirs for uploads
UPLOAD_FOLDER_SOLUTION_CODE = os.path.abspath(os.path.join(UPLOAD_BASE, 'solution_codes'))
UPLOAD_FOLDER_IMAGE = os.path.abspath(os.path.join(os.sep, BASE_DIR, 'app','static','images','profile_pics'))
UPLOAD_FOLDER_TEST = os.path.abspath(os.path.join(os.sep,UPLOAD_BASE, 'large_testcases'))
UPLOAD_FOLDER_PROBLEM = os.path.abspath(os.path.join(os.sep,UPLOAD_BASE, 'problem_text'))
UPLOAD_FOLDER_SUBMISSION= os.path.abspath(os.path.join(os.sep, UPLOAD_BASE, 'user_submissions'))
UPLOAD_FOLDER_EDITORIAL = os.path.abspath(os.path.join(os.sep, UPLOAD_BASE, 'problem_editorials'))
UPLOAD_FOLDER_SANDBOX = os.path.abspath(os.path.join(os.sep, UPLOAD_BASE, '.sandbox'))
UPLOAD_FOLDER_DATASET = os.path.abspath(os.path.join(os.sep, BASE_DIR, 'Datasets'))

# extensions

# for the profile pictue 
ALLOWED_EXTENSIONS_IMAGE = set(['jpg', 'jpeg', 'png'])  
# for the code that is submitted by the users
ALLOWED_EXTENSIONS_CODE  = set(['cpp', 'c', 'py', 'c++'])  
# for the code that is uploaded by the admin 
ALLOWED_EXTENSIONS_SOLUTION_CODE = set(['cpp', 'c', 'c++'])
# for the large test case files 
ALLOWED_EXTENSIONS_TEST  = set(['txt'])
# for the question that is uploaded
ALLOWED_EXTENSIONS_PROBLEM  = set(['txt'])
# for the problem editorial
ALLOWED_EXTENSIONS_EDITORIAL = set(['txt', 'md'])

# Define the database - we are working with

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'safe.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# # Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
