from os import environ

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app, prefix='/api')
CORS(app)