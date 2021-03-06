"""status

Revision ID: 8d22c0e560e9
Revises: cc4fd089a99a
Create Date: 2019-07-10 22:17:24.920454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d22c0e560e9'
down_revision = 'cc4fd089a99a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('status', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'status')
    # ### end Alembic commands ###
