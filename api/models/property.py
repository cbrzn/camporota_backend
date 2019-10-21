import asyncio
from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from api.db.Connection import db, Connection
from api.utils.algolia import create_or_update_property, search_property
from api.utils.cloudinary import upload_images


class Property(db.Model):
    __tablename__ = "properties"

    property_id = db.Column(UUID(as_uuid=True), unique=True,
                            nullable=False, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    kind = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String, nullable=False)
    sale = db.Column(db.Boolean, nullable=False)
    time_created = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def search(cls, params):
        params = ', '.join(params) if type(params) == list else params
        properties = search_property(params)['hits']

        def define_list(row):
            return dict(
                title=row.get('title'),
                description=row.get('description'),
                kind=row.get('kind'),
                price=row.get('price'),
                state=row.get('state'),
                sale=row.get('sale'),
                property_id=row.get('property_id')
            )

        return [define_list(row) for row in properties]

    @classmethod
    def create(cls, files=None, **params):
        try:
            con = Connection()
            new_id = uuid4()
            params['objectID'] = new_id
            create_or_update_property(**params)
            images_path = upload_images(files)
            create_property_query = 'INSERT INTO properties (property_id, title, description, kind, price, state, sale) VALUES (:objectID, :title, :description, :kind, :price, :state, :sale) RETURNING *'
            property_data = asyncio.run(
                con.commit(create_property_query, **params))
            create_images_query = 'INSERT INTO images(property_id, path) VALUES (:property_id, :path)'
            for image in images_path:
                image_data = dict(property_id=property_data["property_id"], path=image['url'])
                asyncio.run(con.commit(create_images_query, **image_data))
            return True
        except BaseException as e:
            print(e)
            return False


class Image(db.Model):
    __tablename__ = "images"

    image_id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    property_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("properties.property_id"))
    image_property = relationship("Property")
