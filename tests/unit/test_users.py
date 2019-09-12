from api.models.user import User
from api.controllers.Users import Users, Authentication

from tests.unit import client

user_resource = Users()
auth_resource = Authentication()
def test_add_user(client):
    response = user_resource.post()
    assert True == bool(response)