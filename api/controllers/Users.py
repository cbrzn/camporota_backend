import asyncio

from flask import jsonify
from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256

from api.models.user import User

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "email", type=str, required=True, help="This field cannot be blank."
)
_user_parser.add_argument(
    "first_name", type=str, required=False, help="This field cannot be blank."
)
_user_parser.add_argument(
    "last_name", type=str, required=False, help="This field cannot be blank."
)
_user_parser.add_argument(
    "password", type=str, required=True, help="This field cannot be blank."
)

class Users(Resource):
    def get(self, email):
        try:
            user = User.find(email)
            return jsonify({ "user": user[0] })
        except:
            return jsonify({ "user": None })
        
    def post(self):
        data = _user_parser.parse_args()
        user_exists = User.find(data['email'])
        if user_exists:
            return jsonify(dict(success=False, message="User already exists"))
        data['password'] = pbkdf2_sha256.hash(data['password'])
        create = User.create(**data)
        return jsonify({ "success": create })

class Authentication(Resource):
    def post(self):
        data = _user_parser.parse_args()
        print(data)
        try:
            user = User.login(**data)
            return jsonify({ "user": user[0] })
        except BaseException as e:
            print(e)
            return jsonify({ "user": None })
