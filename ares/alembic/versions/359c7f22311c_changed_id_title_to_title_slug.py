"""changed id_title to title_slug

Revision ID: 359c7f22311c
Revises: 707954e03604
Create Date: 2023-02-26 10:33:12.197247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '359c7f22311c'
down_revision = '707954e03604'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('section', sa.Column('title_slug', sa.String(), nullable=True))
    op.drop_constraint('section_id_title_key', 'section', type_='unique')
    op.create_unique_constraint(None, 'section', ['title_slug'])
    op.drop_column('section', 'id_title')
    op.add_column('subsection', sa.Column('sub_title_slug', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'subsection', ['sub_title_slug'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'subsection', type_='unique')
    op.drop_column('subsection', 'sub_title_slug')
    op.add_column('section', sa.Column('id_title', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'section', type_='unique')
    op.create_unique_constraint('section_id_title_key', 'section', ['id_title'])
    op.drop_column('section', 'title_slug')
    # ### end Alembic commands ###