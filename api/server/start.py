from os import environ

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
app.config['JWT_SECRET_KEY'] = 'this is my super key'
jwt = JWTManager(app)
api = Api(app, prefix='/api')
CORS(app)