"""empty message

Revision ID: 01863494809b
Revises: c24fa57b95f5
Create Date: 2017-03-04 20:02:37.044881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01863494809b'
down_revision = 'c24fa57b95f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('asset_attacker', sa.Column('wert', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('asset_attacker', 'wert')
    # ### end Alembic commands ###