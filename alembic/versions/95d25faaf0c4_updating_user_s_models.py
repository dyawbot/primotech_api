"""updating user's models

Revision ID: 95d25faaf0c4
Revises: ce72ef53bdeb
Create Date: 2025-02-24 00:45:36.886023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95d25faaf0c4'
down_revision: Union[str, None] = 'ce72ef53bdeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tbl_users', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('tbl_users', sa.Column('last_name', sa.String(), nullable=True))
    op.add_column('tbl_users', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('tbl_users', sa.Column('password', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('tbl_users', 'first_name')
    op.drop_column('tbl_users', 'last_name')
    op.drop_column('tbl_users', 'phone_number')
    op.drop_column('tbl_users', 'password')
