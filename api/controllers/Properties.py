import asyncio
import uuid

from flask import jsonify
from flask_restful import Resource, reqparse

from api.models.property import Property

_property_parser = reqparse.RequestParser()

_property_parser.add_argument("property_id", type=uuid.UUID, required=False)
_property_parser.add_argument("title", type=str, required=False)
_property_parser.add_argument("description", type=str, required=False)
_property_parser.add_argument("kind", type=str, required=False)
_property_parser.add_argument("price", type=int, required=False)
_property_parser.add_argument("state", type=str, required=False)
_property_parser.add_argument("sale", type=bool, required=False)
_property_parser.add_argument("params", required=False)

class Properties(Resource):
    def get(self):
        data = _property_parser.parse_args()
        params = '' if data["params"] == None else data["params"]
        properties = Property.search(params)
        return properties

    def post(self):
        data = _property_parser.parse_args()
        create = Property.create(**data)
        return jsonify({ 'success': create })

    def put(self):
        pass

    def delete(self):
        pass