"""empty message

Revision ID: 294f9978bda7
Revises: 7cc3aa470be7
Create Date: 2020-10-20 19:54:03.895631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '294f9978bda7'
down_revision = '7cc3aa470be7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todos')
    # ### end Alembic commands ###
