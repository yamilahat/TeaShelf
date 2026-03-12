# from app.models import TastingSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer

from app.db.base import Base


class Tea(Base):
    __tablename__ = "teas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    vendor: Mapped[str | None] = mapped_column(String(120), nullable=True)
    origin: Mapped[str | None] = mapped_column(String(120), nullable=True)
    tea_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    harvest_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    tasting_sessions: Mapped[list["TastingSession"]] = relationship(
        back_populates="tea",
        cascade="all, delete-orphan",
    )
