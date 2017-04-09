import sys, string, os, hashlib
from random import randint
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import User
import config

try:
	db.create_all()
except:
	pass
