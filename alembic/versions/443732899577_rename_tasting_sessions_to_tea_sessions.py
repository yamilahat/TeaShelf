"""rename tasting_sessions to tea_sessions

Revision ID: 443732899577
Revises: 1f03d156db7c
Create Date: 2026-03-18 18:11:11.591463
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "443732899577"
down_revision = "1f03d156db7c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    op.add_column("tea_sessions", sa.Column("steeps_count", sa.Integer(), nullable=True))

    missing_session_dates = bind.execute(
        sa.text("SELECT COUNT(*) FROM tea_sessions WHERE session_date IS NULL")
    ).scalar_one()

    if missing_session_dates:
        raise RuntimeError(
            "Cannot make tea_sessions.session_date NOT NULL because existing rows "
            "still have NULL session_date values."
        )

    op.alter_column(
        "tea_sessions",
        "session_date",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
    )



def downgrade() -> None:
    op.alter_column(
        "tea_sessions",
        "session_date",
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
    )
    op.drop_column("tea_sessions", "steeps_count")
