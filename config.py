# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Defining the upload criterion for the various files uploaded by the user

# dirs for uploads
UPLOAD_FOLDER_CODE = os.path.abspath(os.path.join(os.sep, BASE_DIR, 'code_solutions'))
UPLOAD_FOLDER_IMAGE = os.path.abspath(os.path.join(os.sep, BASE_DIR, 'profile_pics'))
UPLOAD_FOLDER_TEST = os.path.abspath(os.path.join(os.sep,BASE_DIR, 'large_testcase'))
UPLOAD_FOLDER_PROBLEM = os.path.abspath(os.path.join(os.sep,BASE_DIR, 'problem_questions'))

#User submissions
UPLOAD_FOLDER_SUBMISSION=os.path.abspath(os.path.join(os.sep,BASE_DIR,'user_submission'))

# extensions
ALLOWED_EXTENSIONS_IMAGE = set(['.jpg', '.jpeg', '.png'])  
ALLOWED_EXTENSIONS_CODE  = set(['.cpp', '.c', '.py'])  
ALLOWED_EXTENSIONS_TEST  = set(['.txt'])

ALLOWED_EXTENSIONS_USER  = set(['.c','.cc','.py'])

# Define the database - we are working with

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'safe.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
