"""adding column timestamp to user and images

Revision ID: de808125f3f7
Revises: 43adeaf081cf
Create Date: 2025-03-25 23:22:45.374374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de808125f3f7'
down_revision: Union[str, None] = '43adeaf081cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    #users
    op.add_column('tbl_users', sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False))
    op.add_column('tbl_users', sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False))
    #images
    op.add_column('tbl_images', sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False))
    op.add_column('tbl_images', sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False))


def downgrade() -> None:

    #users
    op.drop_column('tbl_users', 'created_at')
    op.drop_column('tbl_users', 'updated_at')

    #images
    op.drop_column('tbl_images', 'created_at')
    op.drop_column('tbl_images', 'updated_at')
