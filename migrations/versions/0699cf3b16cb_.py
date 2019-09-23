"""empty message

Revision ID: 0699cf3b16cb
Revises: 73e03cae62aa
Create Date: 2019-09-23 16:27:42.245476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0699cf3b16cb'
down_revision = '73e03cae62aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=True, default=False))
    op.add_column('users', sa.Column('phone', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'admin')
    op.drop_column('users', 'phone')
    # ### end Alembic commands ###
