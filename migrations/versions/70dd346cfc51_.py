"""empty message

Revision ID: 70dd346cfc51
Revises: bc9251478ca5
Create Date: 2020-01-24 11:59:53.258180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70dd346cfc51'
down_revision = 'bc9251478ca5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attendance',
    sa.Column('Attd_ID', sa.Integer(), nullable=False),
    sa.Column('Present', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('Attd_ID')
    )
    op.add_column('course', sa.Column('Classes_held', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('course', 'Classes_held')
    op.drop_table('attendance')
    # ### end Alembic commands ###