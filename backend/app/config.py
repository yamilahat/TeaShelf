"""Application configuration helpers."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "TeaShelf"
    api_prefix: str = "/api"
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/teashelf")


settings = Settings()
