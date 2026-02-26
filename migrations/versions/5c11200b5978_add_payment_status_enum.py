"""add payment status enum

Revision ID: 5c11200b5978
Revises: 2558b6791cb0
Create Date: 2026-02-25 02:34:08.076269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '5c11200b5978'
down_revision: Union[str, Sequence[str], None] = '2558b6791cb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




# 👇 تعريف ENUM
payment_status_enum = sa.Enum(
    'success',
    'failed',
    'pending',
    name='payment_status_enum'
)

def upgrade():
    # 1️⃣ create ENUM type
    payment_status_enum.create(op.get_bind(), checkfirst=True)

    # 2️⃣ add column
    op.add_column(
        'payment',
        sa.Column(
            'status',
            payment_status_enum,
            nullable=False,
            server_default='pending'
        )
    )


def downgrade():
    # 1️⃣ drop column
    op.drop_column('payment', 'status')

    # 2️⃣ drop ENUM type
    payment_status_enum.drop(op.get_bind(), checkfirst=True)