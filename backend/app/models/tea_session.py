import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.tea import Tea
    from app.models.teaware import Teaware


class TeaSession(Base):
    __tablename__ = "tea_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    tea_id: Mapped[int] = mapped_column(
        ForeignKey("teas.id"),
        nullable=False,
        index=True,
    )
    teaware_id: Mapped[int | None] = mapped_column(
        ForeignKey("teaware.id"),
        nullable=True,
        index=True,
    )

    session_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    steeps_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    tea: Mapped["Tea"] = relationship(back_populates="tea_sessions")
    teaware: Mapped["Teaware | None"] = relationship()
