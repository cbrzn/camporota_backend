import asyncio
from flask import jsonify

from api.server.start import instance
from api.db import DatabaseConnection as db

@instance.route('/api')
def all_users():
    con = db()
    users = asyncio.run(con.select("SELECT * FROM users"))
    return jsonify({ 'users': users })

@instance.route('/api/create')
def insert_user():
    con = db()
    query = "INSERT INTO users (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)"
    params = dict(first_name="Cesar", last_name="Brazon", email="cesarbrazon10@gmail.com", password="test")
    worked = asyncio.run(con.commit(query, **params))
    return jsonify({ 'success': worked })