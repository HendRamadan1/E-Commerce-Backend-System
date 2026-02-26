"""init

Revision ID: 517b629c9baf
Revises: 
Create Date: 2026-02-14 23:13:09.361629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = '517b629c9baf'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'customer',
        sa.Column('uid', pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
        sa.Column('FirstName', pg.VARCHAR(), nullable=False),
        sa.Column('MiddleName', pg.VARCHAR(), nullable=False),
        sa.Column('LastName', pg.VARCHAR(), nullable=False),
        sa.Column('Email', pg.VARCHAR(), nullable=False),
        sa.Column('username', pg.VARCHAR(), nullable=False),
        sa.Column('AGE', sa.Integer(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), default=False),
        sa.Column('hassed_password', pg.VARCHAR(), nullable=True),
        sa.Column('DataOfBirth', pg.TIMESTAMP(), nullable=True),
        sa.Column('role', pg.VARCHAR(), nullable=False),
        sa.Column('created_at', pg.TIMESTAMP(), default=datetime.utcnow),
        sa.Column('updated_at', pg.TIMESTAMP(), default=datetime.utcnow)
    )


def downgrade() -> None:
    op.drop_table('customer')
