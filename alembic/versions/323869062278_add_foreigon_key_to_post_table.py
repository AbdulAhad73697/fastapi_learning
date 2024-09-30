"""add foreigon key to post table

Revision ID: 323869062278
Revises: af720aad82ce
Create Date: 2024-09-29 12:18:27.290000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '323869062278'
down_revision: Union[str, None] = 'af720aad82ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id", sa.INTEGER(),nullable=False))
    op.create_foreign_key("post_user_fk",source_table="posts",referent_table="users",
                          local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE"
                          )
    
    pass


def downgrade() -> None:
    op.drop_constraint("post_user_fk",table_name="posts")
    op.drop_column("posts","owner_id")
    pass
