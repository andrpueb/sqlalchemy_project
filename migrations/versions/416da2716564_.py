"""empty message

Revision ID: 416da2716564
Revises: 6db0d53d3baf
Create Date: 2020-10-29 21:36:13.060003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '416da2716564'
down_revision = '6db0d53d3baf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
