import json
import pytest

import api.server.start as app

def test_new_user():
    insert = api.instance.test_client().get('/api/create')
    assert True == json.loads(insert.data)['success']

def test_all_users():
    all_users = [
        {
            "email": "cesarbrazon10@gmail.com", 
            "first_name": "Cesar", 
            "last_name": "Brazon", 
            "password": "test"
        }
    ]
    users = app.instance.test_client().get('/api')
    assert  all_users == json.loads(users.data)['users'] 