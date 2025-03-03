"""Merging branches

Revision ID: 43adeaf081cf
Revises: 8b955862005d
Create Date: 2025-02-24 01:08:00.098866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43adeaf081cf'
down_revision: Union[str, None] = '8b955862005d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE tbl_users SET password = 'hashed_default_password' WHERE password IS NULL")
    op.alter_column('tbl_users', 'password', nullable=False)


def downgrade() -> None:
    pass
