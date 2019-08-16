from flask import Flask
from flask_cors import CORS
from os import environ

instance = Flask(__name__)
CORS(instance)

@instance.route('/')
def hello_wold():
    return "CI done"