"""added unique on model user username

Revision ID: ce72ef53bdeb
Revises: a76dc130afe5
Create Date: 2025-02-11 22:09:29.797828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce72ef53bdeb'
down_revision: Union[str, None] = 'a76dc130afe5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('uq_tbl_users_username', 'tbl_users', ['username'])


def downgrade() -> None:
    op.drop_constraint('uq_tbl_users_usename', 'tbl_users', ['username'])
