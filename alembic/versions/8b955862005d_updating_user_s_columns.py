"""updating user's columns

Revision ID: 8b955862005d
Revises: 95d25faaf0c4
Create Date: 2025-02-24 00:57:20.596850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b955862005d'
down_revision: Union[str, None] = '95d25faaf0c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE tbl_users SET password = 'hashed_default_password' WHERE password IS NULL")
    op.alter_column('tbl_users', 'password', nullable=False)



def downgrade() -> None:
    pass
