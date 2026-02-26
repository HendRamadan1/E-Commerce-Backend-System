"""remove Quantity and price from order_item

Revision ID: 2558b6791cb0
Revises: 13eb081aa39c
Create Date: 2026-02-24 23:41:53.179719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy import Column, Integer, Float


# revision identifiers, used by Alembic.
revision: str = '2558b6791cb0'
down_revision: Union[str, Sequence[str], None] = '13eb081aa39c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



   
def upgrade():
    # drop columns
    op.drop_column('order_item', 'Quantity')
    op.drop_column('order_item', 'price')

def downgrade():
    # add columns back
    op.add_column('order_item', Column('Quantity', Integer))
    op.add_column('order_item', Column('price', Float))
