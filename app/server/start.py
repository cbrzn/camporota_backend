import asyncio

from flask import Flask, jsonify
from flask_cors import CORS

from app.db import DatabaseConnection

instance = Flask(__name__)
CORS(instance)

@instance.route('/api')
def hello_wold():
    con = DatabaseConnection()
    users = asyncio.run(con.select("SELECT * FROM users"))
    return jsonify({'users': users})

@instance.route('/api/create')
def insert_user():
    con = DatabaseConnection()
    query = "INSERT INTO users (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)"
    params = dict(first_name="Cesar", last_name="Brazon", email="cesarbrazon10@gmail.com", password="test")
    worked = asyncio.run(con.commit(query, **params))
    print(worked)
    return "hola"