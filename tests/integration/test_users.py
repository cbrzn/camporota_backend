import json

import pytest
from flask_jwt_extended import create_access_token

import api.server.start as app
from tests.integration import app, mocked_db

mock_user = {
    "email": "cesarbrazon10@gmail.com", 
    "first_name": "Cesar", 
    "last_name": "Brazon",
    "phone":"123456789",
    "admin": False,
    "password": "hey"
}

def test_find(mocked_db):
    user = { 'user': None }
    request = mocked_db.app.test_client().get('/api/user/test@gmail.com')
    assert None == json.loads(request.data)['user']

def test_create(mocked_db):
    json_body = json.dumps(mock_user)
    request = mocked_db.app.test_client().post(
        '/api/user',
        data=json_body,
        content_type='application/json'
    )
    assert True == json.loads(request.data)['success']

def test_login(mocked_db):
    body = dict(email="cesarbrazon10@gmail.com", password="hey")
    json_body = json.dumps(body)
    request = mocked_db.app.test_client().post(
        '/api/login',
        data=json_body,
        content_type='application/json'
    )
    del mock_user['password']
    assert mock_user == json.loads(request.data)['user']
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

def test_logout(mocked_db):
    access_token = create_access_token('test2@gmail.cmom')
    request = mocked_db.app.test_client().delete(
        'api/logout',
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert True == json.loads(request.data)['success']



