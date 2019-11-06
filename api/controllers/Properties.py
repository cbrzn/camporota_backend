import asyncio
import uuid

from flask import jsonify, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

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

    @jwt_required
    def post(self):
        data = _property_parser.parse_args()
        files = request.files.getlist('files[]')
        create = Property.create(files=files, **data)
        return jsonify({ 'success': create })

    @jwt_required
    def put(self):
        pass

    @jwt_required
    def delete(self):
        pass