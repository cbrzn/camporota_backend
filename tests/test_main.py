import app.server.start as app

def test_hello_world():
    test = app.instance.test_client().get('/')
    assert  b'CI done' == test.data

def test_login():
    test = app.instance.test_client().get('/test')
    assert  b'It works' == test.data