"""add teaware table

Revision ID: 9c06c2103db7
Revises: 443732899577
Create Date: 2026-03-21 14:46:53.516501
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c06c2103db7'
down_revision = '443732899577'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'teaware',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(120), nullable=False),
        sa.Column('nickname', sa.String(120), nullable=True),
        sa.Column('type', sa.String(80), nullable=True),
        sa.Column('volume_ml', sa.Integer(), nullable=True),
        sa.Column('material', sa.String(80), nullable=True),
        sa.Column('vendor', sa.String(80), nullable=True),
        sa.Column('acquired_date', sa.Date(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_teaware_name'), 'teaware', ['name'], unique=False)
    op.create_table(
        'teaware_preferred_types',
        sa.Column('teaware_id', sa.Integer(), sa.ForeignKey('teaware.id'), nullable=False),
        sa.Column('tea_type', sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint('teaware_id', 'tea_type'),
    )


def downgrade() -> None:
    op.drop_table('teaware_preferred_types')
    op.drop_index(op.f('ix_teaware_name'), table_name='teaware')
    op.drop_table('teaware')
