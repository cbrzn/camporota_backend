import pytest

import api

@pytest.fixture
def client(mocker):
    mocker.patch("api.controllers.Users.Users.post", return_value=True)