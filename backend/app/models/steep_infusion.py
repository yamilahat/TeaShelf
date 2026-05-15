from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.tea_session import TeaSession


class SteepInfusion(Base):
    __tablename__ = "steep_infusions"
    __table_args__ = (UniqueConstraint("session_id", "steep_number"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("tea_sessions.id"),
        nullable=False,
        index=True,
    )
    steep_number: Mapped[int] = mapped_column(Integer, nullable=False)
    steep_time_seconds: Mapped[int] = mapped_column(Integer, nullable=False)

    session: Mapped["TeaSession"] = relationship(back_populates="steep_infusions")
