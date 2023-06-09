"""Добавили флаг начала работы

Revision ID: eb1863caa2bd
Revises: 
Create Date: 2023-04-07 18:37:37.126725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb1863caa2bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('is_started', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('jobs', 'is_started')
    # ### end Alembic commands ###
