"""empty message

Revision ID: 135d23697059
Revises: 9330c74a2d42
Create Date: 2017-02-27 02:54:17.214034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '135d23697059'
down_revision = '9330c74a2d42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('analyse_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'employees', 'analyses', ['analyse_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'employees', type_='foreignkey')
    op.drop_column('employees', 'analyse_id')
    # ### end Alembic commands ###
