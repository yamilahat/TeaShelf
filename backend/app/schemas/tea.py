from pydantic import BaseModel, ConfigDict

from app.enums import TeaType


class TeaCreate(BaseModel):
    name: str
    vendor: str | None = None
    origin: str | None = None
    tea_type: TeaType | None = None
    harvest_year: int | None = None
    notes: str | None = None


class TeaUpdate(BaseModel):
    name: str
    vendor: str | None = None
    origin: str | None = None
    tea_type: TeaType | None = None
    harvest_year: int | None = None
    notes: str | None = None


class TeaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    vendor: str | None = None
    origin: str | None = None
    tea_type: TeaType | None = None
    harvest_year: int | None = None
    notes: str | None = None
