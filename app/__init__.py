from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    @app.route('/')
    def hello_world():
        return "CI done"

    return app

