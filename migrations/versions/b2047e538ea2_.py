"""empty message

Revision ID: b2047e538ea2
Revises: fea1b4712da8
Create Date: 2020-01-27 16:19:46.054679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2047e538ea2'
down_revision = 'fea1b4712da8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stud_courses',
    sa.Column('stud_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.Course_ID'], ),
    sa.ForeignKeyConstraint(['stud_id'], ['student.stud_id'], )
    )
    op.create_table('ta_courses',
    sa.Column('ta_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.Course_ID'], ),
    sa.ForeignKeyConstraint(['ta_id'], ['TA.TA_id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ta_courses')
    op.drop_table('stud_courses')
    # ### end Alembic commands ###
