import json

import pytest

import api.server.start as app

def test_find():
    user = { 'user': None }
    request = app.app.test_client().get('/api/user/test@gmail.com')
    assert None == json.loads(request.data)['user']

def test_create():
    body = dict(first_name="Cesar", last_name="Brazon", email="cesarbrazon10@gmail.com", password="hey")
    json_body = json.dumps(body)
    request = app.app.test_client().post(
        '/api/user',
        data=json_body,
        content_type='application/json'
    )
    assert True == json.loads(request.data)['success']

def test_login():
    user = {
        "email": "cesarbrazon10@gmail.com", 
        "first_name": "Cesar", 
        "last_name": "Brazon"
    }
    body = dict(email="cesarbrazon10@gmail.com", password="hey")
    json_body = json.dumps(body)
    request = app.app.test_client().post(
        '/api/login',
        data=json_body,
        content_type='application/json'
    )
    assert user == json.loads(request.data)['user']

def test_bad_login():
    body = dict(email="test@gmail.com", password="bad")
    json_body = json.dumps(body)
    request = app.app.test_client().post(
        '/api/login',
        data=json_body,
        content_type='application/json'
    )
    assert None == json.loads(request.data)['user']



