import asyncio
from flask import jsonify
from flask_restful import Resource

from api.models.user import User

class Users(Resource):
    # @app.route('/')
    # def all_users():
    #     con = db()
    #     users = asyncio.run(con.select("SELECT * FROM users"))
    #     return jsonify({ 'users': users })

    def get(self, email):
        try:
            user = User.get_user(email)
            return jsonify({ "user": user[0] })
        except:
            return jsonify({ "user": { } })

    # @app.route('/create')
    # def insert_user():
    #     con = db()
    #     query = "INSERT INTO users (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)"
    #     params = dict(first_name="Cesar", last_name="Brazon", email="cesarbrazon10@gmail.com", password="test")
    #     worked = asyncio.run(con.commit(query, **params))
    #     return jsonify({ 'success': worked })