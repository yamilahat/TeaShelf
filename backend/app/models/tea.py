from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.tea_session import TeaSession


class Tea(Base):
    __tablename__ = "teas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    vendor: Mapped[str | None] = mapped_column(String(120), nullable=True)
    origin: Mapped[str | None] = mapped_column(String(120), nullable=True)
    tea_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    harvest_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    tea_sessions: Mapped[list["TeaSession"]] = relationship(
        back_populates="tea",
        cascade="all, delete-orphan",
    )
