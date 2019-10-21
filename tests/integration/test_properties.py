import json

import pytest

import api.server.start as app
from tests.integration import app, mocked_db
import api.utils.algolia as test

mock_property =  {
    "title": "Top floor",
    "description": "Amazing stuff",
    "kind": "floor",
    "price": 45,
    "state": "Maracaibo",
    "sale": True,
    "property_id": 'ca1ea042-e5db-4746-b453-4a39b832b7fe'
}

def test_create_property(mocked_db, mocker):
    json_body = json.dumps(mock_property)
    mocker.patch('api.models.property.create_or_update_property', return_value=True)
    mocker.patch('api.models.property.upload_images', return_value=[{'url':'first/path.jpg'}, {'url':'second/path.jpg'}])
    request = mocked_db.app.test_client().post(
        'api/properties',
        data=json_body,
        content_type='application/json'
    )
    assert True == json.loads(request.data)['success']

def test_search_property(mocked_db, mocker):
    value = dict(hits=[mock_property])
    mocker.patch('api.models.property.search_property', return_value=value)
    request = mocked_db.app.test_client().get('/api/properties')
    assert json.loads(request.data)[0] == mock_property