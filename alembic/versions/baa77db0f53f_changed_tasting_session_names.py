"""changed tasting_session names

Revision ID: baa77db0f53f
Revises: cd76ba044650
Create Date: 2026-03-12 22:25:14.643271
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "baa77db0f53f"
down_revision = "cd76ba044650"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    op.rename_table("tasting_sessions", "tea_sessions")
    op.execute(
        "ALTER INDEX ix_tasting_sessions_tea_id RENAME TO ix_tea_sessions_tea_id"
    )

    op.add_column(
        "tea_sessions",
        sa.Column("session_date", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "tea_sessions",
        sa.Column("rating", sa.Integer(), nullable=True),
    )

    op.execute(
        "UPDATE tea_sessions SET session_date = brewed_at WHERE brewed_at IS NOT NULL"
    )
    op.execute("UPDATE tea_sessions SET rating = score WHERE score IS NOT NULL")

    missing_session_dates = bind.execute(
        sa.text("SELECT COUNT(*) FROM tea_sessions WHERE session_date IS NULL")
    ).scalar_one()

    if missing_session_dates:
        raise RuntimeError(
            "Cannot make tea_sessions.session_date NOT NULL because existing rows "
            "still have no brewed_at value. Backfill or remove those rows first."
        )

    op.alter_column(
        "tea_sessions",
        "session_date",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
    )

    op.drop_column("tea_sessions", "score")
    op.drop_column("tea_sessions", "brewed_at")



def downgrade() -> None:
    bind = op.get_bind()

    op.add_column(
        "tea_sessions",
        sa.Column("brewed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "tea_sessions",
        sa.Column("score", sa.Integer(), nullable=True),
    )

    op.execute(
        "UPDATE tea_sessions SET brewed_at = session_date WHERE session_date IS NOT NULL"
    )
    op.execute("UPDATE tea_sessions SET score = rating WHERE rating IS NOT NULL")

    missing_brewed_at = bind.execute(
        sa.text("SELECT COUNT(*) FROM tea_sessions WHERE brewed_at IS NULL")
    ).scalar_one()

    if missing_brewed_at:
        raise RuntimeError(
            "Cannot drop tea_sessions.session_date because existing rows still "
            "have no brewed_at value after downgrade backfill."
        )

    op.drop_column("tea_sessions", "rating")
    op.drop_column("tea_sessions", "session_date")

    op.execute(
        "ALTER INDEX ix_tea_sessions_tea_id RENAME TO ix_tasting_sessions_tea_id"
    )
    op.rename_table("tea_sessions", "tasting_sessions")
