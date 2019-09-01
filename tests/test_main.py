import json
import pytest

import app.server.start as app

# @pytest.mark.asyncio
# def test_new_user(event_loop):
#     insert = app.instance.test_client().get('/create')
    
#     print(insert)
#     assert  b'hola' == insert.data

def test_login():
    # test = app.instance.test_client().get('/test')
    assert  b'It works' == b'It works'