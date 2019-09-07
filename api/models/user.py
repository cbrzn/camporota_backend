import asyncio

from api.db.Connection import db, Connection

class User(db.Model):
    __tablename__ = "users"

    email = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    @classmethod
    def get_user(cls, email):
        con = Connection()
        query = "SELECT * FROM users WHERE email = :email"
        params = dict(email=email)
        user = asyncio.run(con.select(query, **params))
        return user
