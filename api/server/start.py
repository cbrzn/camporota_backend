from os import environ

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

instance = Flask(__name__)
instance.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
instance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(instance)
CORS(instance)