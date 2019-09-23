import json

import pytest

import api.server.start as app
from tests.integration import app, mocked_db

def test_find(mocked_db):
    user = { 'user': None }
    request = mocked_db.app.test_client().get('/api/user/test@gmail.com')
    assert None == json.loads(request.data)['user']

def test_create(mocked_db):
    body = dict(first_name="Cesar", last_name="Brazon", email="cesarbrazon10@gmail.com", password="hey", phone="123456789")
    json_body = json.dumps(body)
    request = mocked_db.app.test_client().post(
        '/api/user',
        data=json_body,
        content_type='application/json'
    )
    assert True == json.loads(request.data)['success']

def test_login(mocked_db):
    user = {
        "email": "cesarbrazon10@gmail.com", 
        "first_name": "Cesar", 
        "last_name": "Brazon",
        "phone":"123456789",
        "admin": False
    }
    body = dict(email="cesarbrazon10@gmail.com", password="hey")
    json_body = json.dumps(body)
    request = mocked_db.app.test_client().post(
        '/api/login',
        data=json_body,
        content_type='application/json'
    )
    print(json.loads(request.data))
    assert user == json.loads(request.data)['user']
    assert type(json.loads(request.data)['access_token']) is str

def test_bad_login(mocked_db):
    body = dict(email="test@gmail.com", password="bad")
    json_body = json.dumps(body)
    request = mocked_db.app.test_client().post(
        '/api/login',
        data=json_body,
        content_type='application/json'
    )
    assert None == json.loads(request.data)['user']



