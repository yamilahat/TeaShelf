from datetime import datetime

from sqlalchemy import ForeignKey, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
# from app.models import Tea


class TastingSession(Base):
    __tablename__ = "tasting_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    tea_id: Mapped[int] = mapped_column(ForeignKey("teas.id"), nullable=False, index=True)

    session_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    tea: Mapped["Tea"] = relationship(back_populates="tasting_sessions")
