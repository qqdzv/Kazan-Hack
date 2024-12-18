"""empty message

Revision ID: 2896871093f6
Revises: 134afded54c5
Create Date: 2024-11-23 06:44:10.058641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2896871093f6'
down_revision: Union[str, None] = '134afded54c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medcard',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('type_analysis', sa.String(), nullable=True),
    sa.Column('data', sa.TIMESTAMP(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_medcard_id'), 'medcard', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_medcard_id'), table_name='medcard')
    op.drop_table('medcard')
    # ### end Alembic commands ###
