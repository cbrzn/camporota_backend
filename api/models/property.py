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

    rooms = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String, nullable=True)
    square_meters = db.Column(db.Integer, nullable=True)
    heating = db.Column(db.Boolean, nullable=True)
    community_fees = db.Column(db.String, nullable=True)
    orientation = db.Column(db.String, nullable=True)
    furnished = db.Column(db.Boolean, nullable=True)
    equipped_kitchen = db.Column(db.Boolean, nullable=True)
    floor_number = db.Column(db.String, nullable=True)
    common_zones = db.Column(db.String, nullable=True)
    pets = db.Column(db.Boolean, nullable=True)
    contract_time = db.Column(db.String, nullable=True)
    bond = db.Column(db.String, nullable=True)

    time_created = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def search(cls, location, kind, price_min, price_max, sale, address, bathrooms, rooms, furnished):
        properties = search_property(
            location, kind, price_min, price_max, sale, address, bathrooms, rooms, furnished)['hits']

        def define_list(row):
            return dict(
                title=row.get('title'),
                description=row.get('description'),
                kind=row.get('kind'),
                price=row.get('price'),
                state=row.get('state'),
                sale=row.get('sale'),
                bathrooms=row.get('bathrooms'),
                rooms=row.get('rooms'),
                address=row.get('address'),
                square_meters=row.get('square_meters'),
                heating=row.get('heating'),
                community_fees=row.get('community_fees'),
                orientation=row.get('orientation'),
                furnished=row.get('furnished'),
                equipped_kitchen=row.get('equipped_kitchen'),
                floor_number=row.get('floor_number'),
                common_zones=row.get('common_zones'),
                pets=row.get('pets'),
                contract_time=row.get('contract_time'),
                bond=row.get('bond'),
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
            create_property_query = 'INSERT INTO properties (property_id, title, description, kind, price, state, sale, bathrooms, rooms, address, square_meters, heating, community_fees, orientation, furnished, equipped_kitchen, floor_number, common_zones, pets, contract_time, bond) VALUES (:objectID, :title, :description, :kind, :price, :state, :sale, :bathrooms, :rooms, :address, :square_meters, :heating, :community_fees, :orientation, :furnished, :equipped_kitchen, :floor_number, :common_zones, :pets, :contract_time, :bond) RETURNING *'
            property_data = asyncio.run(
                con.commit(create_property_query, **params))
            create_images_query = 'INSERT INTO images(property_id, path) VALUES (:property_id, :path)'
            for image in images_path:
                image_data = dict(
                    property_id=property_data["property_id"], path=image['url'])
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
            is_deleted = asyncio.run(con.commit(
                delete_property_query, **dict(property_id=property_id)))
            return is_deleted
        except:
            return False

    @classmethod
    def update(cls, files=None, **params):
        try:
            con = Connection()
            select_property_query = 'SELECT * FROM properties WHERE property_id = :property_id'
            property_attributes = asyncio.run(
                con.select(select_property_query, **params))[0]
            new_attributes = dict()
            title = property_attributes['title']
            description = property_attributes['description']
            kind = property_attributes['kind']
            price = property_attributes['price']
            state = property_attributes['state']
            sale = property_attributes['sale']

            rooms = property_attributes['rooms']
            bathrooms = property_attributes['bathrooms']
            address = property_attributes['address']
            square_meters = property_attributes['square_meters']
            heating = property_attributes['heating']
            community_fees = property_attributes['community_fees']
            orientation = property_attributes['orientation']
            furnished = property_attributes['furnished']
            equipped_kitchen = property_attributes['equipped_kitchen']
            floor_number = property_attributes['floor_number']
            common_zones = property_attributes['common_zones']
            contract_time = property_attributes['contract_time']
            bond = property_attributes['bond']
            pets = property_attributes['pets']

            new_attributes['title'] = title if params['title'] == title or params['title'] == None else params['title']
            new_attributes['description'] = description if params['description'] == description or params['description'] == None else params['description']
            new_attributes['kind'] = kind if params['kind'] == kind or params['kind'] == None else params['kind']
            new_attributes['price'] = price if params['price'] == price or params['price'] == None else params['price']
            new_attributes['state'] = state if params['state'] == state or params['state'] == None else params['state']
            new_attributes['sale'] = sale if params['sale'] == sale or params['sale'] == None else params['sale']

            new_attributes['rooms'] = rooms if params['rooms'] == rooms or params['rooms'] == None else params['rooms']
            new_attributes['bathrooms'] = bathrooms if params['bathrooms'] == bathrooms or params['bathrooms'] == None else params['bathrooms']
            new_attributes['address'] = address if params['address'] == address or params['address'] == None else params['address']
            new_attributes['square_meters'] = square_meters if params['square_meters'] == square_meters or params['square_meters'] == None else params['square_meters']
            new_attributes['heating'] = heating if params['heating'] == heating or params['heating'] == None else params['heating']
            new_attributes['community_fees'] = community_fees if params[
                'community_fees'] == community_fees or params['community_fees'] == None else params['community_fees']
            new_attributes['orientation'] = orientation if params['orientation'] == orientation or params['orientation'] == None else params['orientation']
            new_attributes['furnished'] = furnished if params['furnished'] == furnished or params['furnished'] == None else params['furnished']
            new_attributes['equipped_kitchen'] = equipped_kitchen if params[
                'equipped_kitchen'] == equipped_kitchen or params['equipped_kitchen'] == None else params['equipped_kitchen']
            new_attributes['floor_number'] = floor_number if params['floor_number'] == floor_number or params['floor_number'] == None else params['floor_number']
            new_attributes['common_zones'] = common_zones if params['common_zones'] == common_zones or params['common_zones'] == None else params['common_zones']
            new_attributes['pets'] = pets if params['pets'] == pets or params['pets'] == None else params['pets']
            new_attributes['contract_time'] = contract_time if params['contract_time'] == contract_time or params['contract_time'] == None else params['contract_time']
            new_attributes['bond'] = bond if params['bond'] == bond or params['bond'] == None else params['bond']

            new_attributes['objectID'] = params['property_id']
            create_or_update_property(**new_attributes)
            update_property_query = 'UPDATE properties SET title = :title, description = :description, kind = :kind, price = :price, state = :state, sale = :sale, bathrooms = :bathrooms, rooms = :rooms, address = :address, square_meters = :square_meters, heating = :heating, community_fees = :community_fees, orientation = :orientation, furnished = :furnished, equipped_kitchen = :equipped_kitchen, floor_number = :floor_number, common_zones = :common_zones, pets = :pets, contract_time = :contract_time, bond = :bond WHERE property_id = :objectID'
            updated = asyncio.run(con.commit(
                update_property_query, **new_attributes))
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
    image_property = relationship(
        "Property", backref=backref('image', passive_deletes=True))
