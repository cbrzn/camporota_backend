import asyncio
from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref

from api.db.Connection import db, Connection
from api.utils.algolia import create_or_update_property, search_property, delete_property
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
    # room = db.Column(db.Integer, nullable=True)
    # bathroom = db.Column(db.Integer, nullable=True)
    time_created = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def search(cls, location, kind, price_min, price_max, sale):
        properties = search_property(location, kind, price_min, price_max, sale)['hits']

        def define_list(row):
            return dict(
                title=row.get('title'),
                description=row.get('description'),
                kind=row.get('kind'),
                price=row.get('price'),
                state=row.get('state'),
                sale=row.get('sale'),
                # bathroom=row.get('bathroom'),
                # room=row.get('room'),
                property_id=row.get('objectID'),
                images=Property.images(row.get('objectID'))
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

    @classmethod
    def delete(cls, property_id):
        try:
            con = Connection()
            delete_property(property_id)
            delete_property_query = 'DELETE FROM properties WHERE property_id = :property_id'
            is_deleted = asyncio.run(con.commit(delete_property_query, **dict(property_id=property_id)))
            return is_deleted
        except:
            return False
        

    @classmethod
    def update(cls, files=None, **params):
        try:
            con = Connection()
            select_property_query = 'SELECT * FROM properties WHERE property_id = :property_id'
            property_attributes = asyncio.run(con.select(select_property_query, **params))[0]
            new_attributes = dict()
            title = property_attributes['title']
            description = property_attributes['description']
            kind = property_attributes['kind']
            price = property_attributes['price']
            state = property_attributes['state']
            sale = property_attributes['sale']
            # room = property_attributes['room']
            # bathroom = property_attributes['bathroom']
            new_attributes['title'] = title if params['title'] == title or params['title'] == None else params['title']
            new_attributes['description'] = description if params['description'] == description or params['description'] == None else params['description']
            new_attributes['kind'] = kind if params['kind'] == kind or params['kind'] == None else params['kind']
            new_attributes['price'] = price if params['price'] == price or params['price'] == None else params['price']
            new_attributes['state'] = state if params['state'] == state or params['state'] == None else params['state']
            new_attributes['sale'] = sale if params['sale'] == sale or params['sale'] == None else params['sale']
            # new_attributes['room'] = room if params['room'] == room or params['room'] == None else params['room']
            # new_attributes['bathroom'] = bathroom if params['bathroom'] == bathroom or params['bathroom'] == None else params['bathroom']
            new_attributes['objectID'] = params['property_id']
            create_or_update_property(**new_attributes)
            update_property_query = 'UPDATE properties SET title = :title, description = :description, kind = :kind, price = :price, state = :state, sale = :sale WHERE property_id = :objectID'
            updated = asyncio.run(con.commit(update_property_query, **new_attributes))
            return updated
        except Exception as e:
            print(e)
            return False

    @classmethod
    def images(cls, property_id):
        con = Connection()
        query = 'SELECT images.path FROM properties INNER JOIN images ON images.property_id = properties.property_id WHERE properties.property_id = :id'
        images = asyncio.run(con.select(query, **dict(id=property_id)))
        return images

class Image(db.Model):
    __tablename__ = "images"

    image_id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    property_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("properties.property_id", ondelete="CASCADE"))
    image_property = relationship("Property", backref=backref('image', passive_deletes=True))
