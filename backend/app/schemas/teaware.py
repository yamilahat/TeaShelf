from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator


class TeawareBase(BaseModel):
    name: str
    nickname: str | None = None
    type: str | None = None
    volume_ml: int | None = None
    material: str | None = None
    vendor: str | None = None
    preferred_tea_types: list[str] = []
    acquired_date: date | None = None
    notes: str | None = None

    @field_validator("acquired_date", mode="before")
    @classmethod
    def parse_acquired_date(cls, value: object) -> object:
        if isinstance(value, str) and value:
            for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
            raise ValueError(f"Invalid date format: {value!r}. Use DD/MM/YYYY.")
        return value


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
        if value and hasattr(value[0], "tea_type_ref"):
            return [item.tea_type_ref.name for item in value]
        return value

    @field_serializer("acquired_date")
    def serialize_acquired_date(self, value: date | None) -> str | None:
        if value is None:
            return None
        return value.strftime("%d/%m/%Y")
