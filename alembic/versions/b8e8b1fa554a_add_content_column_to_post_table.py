"""add content column to post table 

Revision ID: b8e8b1fa554a
Revises: c56a696ec9f5
Create Date: 2024-09-29 11:24:49.614662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8e8b1fa554a'
down_revision: Union[str, None] = 'c56a696ec9f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
