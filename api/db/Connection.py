import asyncio
from os import environ

from sqlalchemy_aio import ASYNCIO_STRATEGY
from sqlalchemy import create_engine, text
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from api.server.start import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Connection():
    def __init__(self):
        self.engine = create_engine(environ.get("DATABASE_URL"), strategy=ASYNCIO_STRATEGY)

    async def select(self, query, **kwargs):
        async with self.engine.connect() as conn:
            async with conn.begin():
                result_object = await conn.execute(text(query), **kwargs)
                result = await result_object.fetchall()
                return [dict(row) for row in result]

    async def commit(self, query, **kwargs):
        try:
            async with self.engine.connect() as conn:
                async with conn.begin():
                    await conn.execute(text(query), kwargs)
                    return True
        except:
            return False