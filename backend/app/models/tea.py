from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.tea_session import TeaSession
    from app.models.tea_type import TeaTypeRef


class Tea(Base):
    __tablename__ = "teas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    vendor: Mapped[str | None] = mapped_column(String(120), nullable=True)
    origin: Mapped[str | None] = mapped_column(String(120), nullable=True)
    tea_type_id: Mapped[int | None] = mapped_column(
        ForeignKey("tea_types.id"), nullable=True
    )
    harvest_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    tea_type_ref: Mapped["TeaTypeRef | None"] = relationship()
    tea_sessions: Mapped[list["TeaSession"]] = relationship(
        back_populates="tea",
        cascade="all, delete-orphan",
    )

    @property
    def tea_type(self) -> str | None:
        return self.tea_type_ref.name if self.tea_type_ref else None
