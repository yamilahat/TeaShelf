from datetime import date

from pydantic import BaseModel, ConfigDict


class TeawareBase(BaseModel):
    name: str
    nickname: str | None = None
    type: str | None = None
    volume_ml: int | None = None
    material: str | None = None
    vendor: str | None = None
    preferred_tea_id: int | None = None
    acquired_date: date | None = None
    notes: str | None = None


class TeawareCreate(TeawareBase):
    pass


class TeawareUpdate(TeawareBase):
    pass


class TeawareRead(TeawareBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
