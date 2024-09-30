"""create posts table

Revision ID: c56a696ec9f5
Revises: 
Create Date: 2024-09-29 05:37:34.745264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c56a696ec9f5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
       op.create_table("posts",sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
                       sa.Column("title",sa.String(),nullable=False)
       )
   
       pass

def downgrade() -> None:
  op.drop_table("posts")
  pass
