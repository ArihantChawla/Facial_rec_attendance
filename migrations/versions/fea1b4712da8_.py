"""empty message

Revision ID: fea1b4712da8
Revises: 70dd346cfc51
Create Date: 2020-01-27 12:29:43.723538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fea1b4712da8'
down_revision = '70dd346cfc51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attendance', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_attendance_timestamp'), 'attendance', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_attendance_timestamp'), table_name='attendance')
    op.drop_column('attendance', 'timestamp')
    # ### end Alembic commands ###
