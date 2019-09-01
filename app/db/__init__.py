import asyncio
from os import environ

from sqlalchemy_aio import ASYNCIO_STRATEGY
from sqlalchemy import create_engine, text

db_uri = environ.get("DATABASE_URL")

class DatabaseConnection():
    def __init__(self):
        self.engine = create_engine(db_uri, strategy=ASYNCIO_STRATEGY)
        print(self.engine)

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
