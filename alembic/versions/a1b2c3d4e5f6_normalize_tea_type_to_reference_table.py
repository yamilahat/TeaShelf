"""normalize tea_type to reference table

Revision ID: a1b2c3d4e5f6
Revises: 5a98ed696749
Create Date: 2026-03-21 20:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "a1b2c3d4e5f6"
down_revision = "5a98ed696749"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Phase A: Create and seed tea_types table
    tea_types_table = op.create_table(
        "tea_types",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), unique=True, nullable=False, index=True),
        sa.Column("category", sa.String(50), nullable=False),
    )
    op.bulk_insert(
        tea_types_table,
        [
            {"id": 1, "name": "green", "category": "green"},
            {"id": 2, "name": "white", "category": "white"},
            {"id": 3, "name": "black", "category": "black"},
            {"id": 4, "name": "red", "category": "red"},
            {"id": 5, "name": "yellow", "category": "yellow"},
            {"id": 6, "name": "oolong", "category": "oolong"},
            {"id": 7, "name": "shou pu-erh (ripe)", "category": "pu-erh"},
            {"id": 8, "name": "sheng pu-erh (raw)", "category": "pu-erh"},
        ],
    )

    # Phase B: Migrate teas table
    op.add_column("teas", sa.Column("tea_type_id", sa.Integer, nullable=True))
    op.execute(
        "UPDATE teas SET tea_type_id = tea_types.id "
        "FROM tea_types WHERE teas.tea_type = tea_types.name"
    )
    op.drop_column("teas", "tea_type")
    op.create_foreign_key(
        "fk_teas_tea_type_id", "teas", "tea_types", ["tea_type_id"], ["id"]
    )

    # Phase C: Migrate teaware_preferred_types table
    op.add_column(
        "teaware_preferred_types",
        sa.Column("tea_type_id", sa.Integer, nullable=True),
    )
    op.execute(
        "UPDATE teaware_preferred_types SET tea_type_id = tea_types.id "
        "FROM tea_types WHERE teaware_preferred_types.tea_type = tea_types.name"
    )
    # Drop old composite PK, then the tea_type column
    op.execute(
        "ALTER TABLE teaware_preferred_types "
        "DROP CONSTRAINT teaware_preferred_types_pkey"
    )
    op.drop_column("teaware_preferred_types", "tea_type")
    op.alter_column(
        "teaware_preferred_types", "tea_type_id", nullable=False
    )
    op.create_primary_key(
        "teaware_preferred_types_pkey",
        "teaware_preferred_types",
        ["teaware_id", "tea_type_id"],
    )
    op.create_foreign_key(
        "fk_teaware_preferred_types_tea_type_id",
        "teaware_preferred_types",
        "tea_types",
        ["tea_type_id"],
        ["id"],
    )


def downgrade() -> None:
    # Reverse Phase C
    op.add_column(
        "teaware_preferred_types",
        sa.Column("tea_type", sa.String(50), nullable=True),
    )
    op.execute(
        "UPDATE teaware_preferred_types SET tea_type = tea_types.name "
        "FROM tea_types WHERE teaware_preferred_types.tea_type_id = tea_types.id"
    )
    op.drop_constraint(
        "fk_teaware_preferred_types_tea_type_id",
        "teaware_preferred_types",
        type_="foreignkey",
    )
    op.execute(
        "ALTER TABLE teaware_preferred_types "
        "DROP CONSTRAINT teaware_preferred_types_pkey"
    )
    op.drop_column("teaware_preferred_types", "tea_type_id")
    op.alter_column(
        "teaware_preferred_types", "tea_type", nullable=False
    )
    op.create_primary_key(
        "teaware_preferred_types_pkey",
        "teaware_preferred_types",
        ["teaware_id", "tea_type"],
    )

    # Reverse Phase B
    op.add_column(
        "teas", sa.Column("tea_type", sa.String(50), nullable=True)
    )
    op.execute(
        "UPDATE teas SET tea_type = tea_types.name "
        "FROM tea_types WHERE teas.tea_type_id = tea_types.id"
    )
    op.drop_constraint("fk_teas_tea_type_id", "teas", type_="foreignkey")
    op.drop_column("teas", "tea_type_id")

    # Reverse Phase A
    op.drop_table("tea_types")
