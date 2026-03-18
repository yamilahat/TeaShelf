from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import UTCDateTime

if TYPE_CHECKING:
    from app.models.tea import Tea


class TeaSession(Base):
    __tablename__ = "tea_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    tea_id: Mapped[int] = mapped_column(
        ForeignKey("teas.id"),
        nullable=False,
        index=True,
    )

    session_date: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
    steeps_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    tea: Mapped["Tea"] = relationship(back_populates="tea_sessions")
