import datetime

from sqlalchemy import ForeignKey, String, Text, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TeawarePreferredType(Base):
    __tablename__ = "teaware_preferred_types"

    teaware_id: Mapped[int] = mapped_column(ForeignKey("teaware.id"), primary_key=True)
    tea_type: Mapped[str] = mapped_column(String(50), primary_key=True)


class Teaware(Base):
    __tablename__ = "teaware"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    nickname: Mapped[str | None] = mapped_column(String(120), nullable=True)
    type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    volume_ml: Mapped[int | None] = mapped_column(Integer, nullable=True)
    material: Mapped[str | None] = mapped_column(String(80), nullable=True)
    vendor: Mapped[str | None] = mapped_column(String(80), nullable=True)
    acquired_date: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    preferred_tea_types: Mapped[list["TeawarePreferredType"]] = relationship(
        cascade="all, delete-orphan"
    )
