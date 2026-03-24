"""add quantity columns to teas

Revision ID: b3c4d5e6f7a8
Revises: a1b2c3d4e5f6
Create Date: 2026-03-24 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

revision = "b3c4d5e6f7a8"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("teas", sa.Column("initial_quantity_g", sa.Float(), nullable=True))
    op.add_column("teas", sa.Column("current_quantity_g", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("teas", "current_quantity_g")
    op.drop_column("teas", "initial_quantity_g")
