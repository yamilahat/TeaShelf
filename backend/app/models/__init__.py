"""Application models package.

Add model modules here and import them in this package so Alembic can see
all registered metadata before autogenerating migrations.
"""

from app.db.base import Base
from app.models.tea import Tea

__all__ = ["Base", "Tea"]
