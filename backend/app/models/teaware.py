import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.tea import Tea


class Teaware(Base):
    __tablename__ = "teaware"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    nickname: Mapped[str | None] = mapped_column(String(120), nullable=True)
    type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    volume_ml: Mapped[int | None] = mapped_column(Integer, nullable=True)
    material: Mapped[str | None] = mapped_column(String(80), nullable=True)
    vendor: Mapped[str | None] = mapped_column(String(80), nullable=True)
    preferred_tea_id: Mapped[int | None] = mapped_column(
        ForeignKey("teas.id"), nullable=True, index=True
    )
    acquired_date: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    preferred_tea: Mapped["Tea | None"] = relationship()
