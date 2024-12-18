"""empty message

Revision ID: 3adbc422f349
Revises: 55e57614232e
Create Date: 2024-11-22 13:45:51.910508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3adbc422f349'
down_revision: Union[str, None] = '55e57614232e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('conference_time', sa.TIMESTAMP(), nullable=True))
    op.add_column('message', sa.Column('have_link', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'have_link')
    op.drop_column('message', 'conference_time')
    # ### end Alembic commands ###
