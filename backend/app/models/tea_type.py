from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

TEA_TYPE_SEEDS = [
    {"id": 1, "name": "green", "category": "green"},
    {"id": 2, "name": "white", "category": "white"},
    {"id": 3, "name": "black", "category": "black"},
    {"id": 4, "name": "red", "category": "red"},
    {"id": 5, "name": "yellow", "category": "yellow"},
    {"id": 6, "name": "oolong", "category": "oolong"},
    {"id": 7, "name": "shou pu-erh (ripe)", "category": "pu-erh"},
    {"id": 8, "name": "sheng pu-erh (raw)", "category": "pu-erh"},
]


class TeaTypeRef(Base):
    __tablename__ = "tea_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
