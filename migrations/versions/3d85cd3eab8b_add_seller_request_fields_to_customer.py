"""add seller request fields to customer

Revision ID: 3d85cd3eab8b
Revises: b7612e57cd59
Create Date: 2026-02-18 15:15:36.013232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '3d85cd3eab8b'
down_revision: Union[str, Sequence[str], None] = 'b7612e57cd59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
   
    op.add_column('customer', sa.Column('requested_store_name', sa.String(), nullable=True))
    op.add_column('customer', sa.Column('requested_phone', sa.String(), nullable=True))

def downgrade():
 
    op.drop_column('customer', 'requested_store_name')
    op.drop_column('customer', 'requested_phone')

