"""created role column

Revision ID: 44379fd7854a
Revises: 7493be6a7819
Create Date: 2023-01-11 20:51:08.571698

"""
from alembic import op
import sqlalchemy as sa


from athena.api.database.models.user_model import RoleEnum


# revision identifiers, used by Alembic.
revision = '44379fd7854a'
down_revision = '7493be6a7819'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    role = sa.Enum(RoleEnum, name='roleenum')
    role.create(op.get_bind(), checkfirst=True)
    op.add_column('user', sa.Column('role', sa.Enum('admin', 'user', 'superuser', name='roleenum'), server_default='user', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    role = sa.Enum(RoleEnum, name='roleenum')
    role.drop(op.get_bind())
    # ### end Alembic commands ###