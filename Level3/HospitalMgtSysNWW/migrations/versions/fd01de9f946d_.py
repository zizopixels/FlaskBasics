"""empty message

Revision ID: fd01de9f946d
Revises: 3d1e2782190c
Create Date: 2019-12-21 17:02:21.902493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd01de9f946d'
down_revision = '3d1e2782190c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('post_ibfk_3', 'post', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('post_ibfk_3', 'post', 'medicalstaff', ['tostaff_ID'], ['StaffID'])
    # ### end Alembic commands ###
