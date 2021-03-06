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

_property_parser.add_argument("rooms", required=False)
_property_parser.add_argument("bathrooms", required=False)
_property_parser.add_argument("square_meters", required=False)
_property_parser.add_argument("heating", required=False)
_property_parser.add_argument("community_fees", required=False)
_property_parser.add_argument("orientation", required=False)
_property_parser.add_argument("equipped_kitchen", required=False)
_property_parser.add_argument("floor_number", required=False)
_property_parser.add_argument("common_zones", required=False)
_property_parser.add_argument("pets", required=False)
_property_parser.add_argument("contract_time", required=False)
_property_parser.add_argument("bond", required=False)
_property_parser.add_argument("address", required=False)
_property_parser.add_argument("furnished", required=False)
_property_parser.add_argument("sale", required=False)
_property_parser.add_argument("location", required=False)
_property_parser.add_argument("price_min", required=False)
_property_parser.add_argument("price_max", required=False)
_property_parser.add_argument("type", required=False)

class Properties(Resource):
    def get(self):
        data = _property_parser.parse_args()
        location = None if data["location"] == None else data["location"]
        kind = None if data["type"] == None else data["type"]
        price_min = None if data["price_min"] == None else data["price_min"]
        price_max = None if data["price_max"] == None else data["price_max"]
        sale = None if data["sale"] == None else data["sale"]
        address = None if data["address"] == None else data["address"]
        bathrooms = None if data["bathrooms"] == None else data["bathrooms"]
        rooms = None if data["rooms"] == None else data["rooms"]
        furnished = None if data["furnished"] == None else data["furnished"]
        properties = Property.search(location, kind, price_min, price_max, sale, address, bathrooms, rooms, furnished)
        return properties

    @jwt_required
    def post(self):
        data = _property_parser.parse_args()
        files = request.files.getlist('files[]')
        create = Property.create(files=files, **data)
        return jsonify({ 'success': create })

    @jwt_required
    def put(self):
        data = _property_parser.parse_args()
        files = request.files.getlist('files[]')
        update = Property.update(files=files, **data)
        return jsonify({ 'success': update })

    @jwt_required
    def delete(self):
        data = _property_parser.parse_args()
        is_deleted = Property.delete(data["property_id"])
        return jsonify({ 'success': is_deleted })
            