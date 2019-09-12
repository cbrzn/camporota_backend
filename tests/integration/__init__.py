from os import environ

import pytest

import api.server.start as instance
from api.db.Connection import db, Connection

@pytest.fixture(scope='session')
def app(request):
    app_test = instance.app
    app_test.config['TESTING'] = True
    app_test.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres@127.0.0.1:5432/testing_db")
    environ['DATABASE_URL'] = "postgres://postgres@127.0.0.1:5432/testing_db")

    ctx = app_test.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app_test

@pytest.fixture(scope='session')
def mocked_db(app, request):
    db.app = app
    db.create_all()

    def teardown():
        db.drop_all()

    request.addfinalizer(teardown)
    return db
