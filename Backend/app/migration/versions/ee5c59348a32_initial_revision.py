"""Initial revision

Revision ID: ee5c59348a32
Revises: bd56899a74e6
Create Date: 2025-03-09 02:21:20.665504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee5c59348a32'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('phone_number', sa.VARCHAR(), server_default=sa.text('0'), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('phone_number', name='users_phone_number_key')
    )


def downgrade() -> None:
    op.drop_table('users')
