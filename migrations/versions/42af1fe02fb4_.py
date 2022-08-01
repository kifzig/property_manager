"""empty message

Revision ID: 42af1fe02fb4
Revises: 
Create Date: 2022-07-30 07:44:11.654693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42af1fe02fb4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('properties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=250), nullable=False),
    sa.Column('tenant_name', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('address')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('properties')
    # ### end Alembic commands ###
