from sqlalchemy import Table, Column, Integer, String, MetaData

meta = MetaData()

users = Table(
    'users', meta,
    Column('email', String(30), primary_key=True),
    Column('first_name', String(20)),
    Column('last_name', String(20)),
    Column('password', String)
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    users.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    users.drop()
