from api.server.start import instance, db


class User(db.Model):
    __tablename__ = "users"

    email = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

