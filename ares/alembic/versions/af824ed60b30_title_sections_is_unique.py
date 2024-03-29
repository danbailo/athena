"""title sections is unique

Revision ID: af824ed60b30
Revises: 03d7ca3edfd1
Create Date: 2023-02-25 15:44:51.575927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af824ed60b30'
down_revision = '03d7ca3edfd1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'section', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'section', type_='unique')
    # ### end Alembic commands ###
