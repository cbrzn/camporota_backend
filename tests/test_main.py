import app

def test_hello_world():
    test = app.create_app().test_client().get('/')
    assert  b'We up' == test.data