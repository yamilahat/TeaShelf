"""Database wiring lives here once persistence is added."""

from app.config import settings


def get_database_url() -> str:
    return settings.database_url
