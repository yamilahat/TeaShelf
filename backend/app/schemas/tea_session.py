from tkinter import N

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SessionCreate(BaseModel):
    tea_id: int
    session_date: datetime
    steeps_count: int | None = None
    rating: int | None = None
    notes: str | None = None


class SessionUpdate(BaseModel):
    tea_id: int
    session_date: datetime
    steeps_count: int | None = None
    rating: int | None = None
    notes: str | None = None


class SessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tea_id: int
    session_date: datetime
    steeps_count: int | None = None
    rating: int | None = None
    notes: str | None = None
