"""add users table

Revision ID: af720aad82ce
Revises: b8e8b1fa554a
Create Date: 2024-09-29 11:55:58.151232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af720aad82ce'
down_revision: Union[str, None] = 'b8e8b1fa554a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id",sa.Integer(),nullable=False),
                    sa.Column("email",sa.String(),nullable=False),
                    sa.Column("password",sa.INTEGER(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()"),nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
