from datetime import date

from pydantic import BaseModel, ConfigDict, field_validator

from app.enums import TeaType


class TeawareBase(BaseModel):
    name: str
    nickname: str | None = None
    type: str | None = None
    volume_ml: int | None = None
    material: str | None = None
    vendor: str | None = None
    preferred_tea_types: list[TeaType] = []
    acquired_date: date | None = None
    notes: str | None = None


class TeawareCreate(TeawareBase):
    pass


class TeawareUpdate(TeawareBase):
    pass


class TeawareRead(TeawareBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    @field_validator("preferred_tea_types", mode="before")
    @classmethod
    def extract_tea_types(cls, value: object) -> object:
        if value and hasattr(value[0], "tea_type"):
            return [item.tea_type for item in value]
        return value
