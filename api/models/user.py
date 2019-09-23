import asyncio

from passlib.hash import pbkdf2_sha256

from api.db.Connection import db, Connection

class User(db.Model):
    __tablename__ = "users"

    email = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String, nullable=False)

    @classmethod
    def find(cls, email):
        con = Connection()
        query = "SELECT * FROM users WHERE email = :email"
        params = dict(email=email)
        user = asyncio.run(con.select(query, **params))
        return user

    @classmethod
    def create(cls, **params):
        con = Connection()
        admin = True if params.get('admin') else False
        params['admin'] = admin
        print(params)
        query = "INSERT INTO users (first_name, last_name, email, password, phone, admin) VALUES (:first_name, :last_name, :email, :password, :phone, :admin)"
        success = asyncio.run(con.commit(query, **params))
        return success

    @classmethod
    def login(cls, **params):
        con = Connection()
        get_hash_query = "SELECT * FROM users WHERE email = :email"
        user = asyncio.run(con.select(get_hash_query, **params))
        if pbkdf2_sha256.verify(params['password'], user[0]['password']):
            del user[0]['password']
            return user[0]

        return None