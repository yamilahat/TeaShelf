from datetime import date

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator

from app.schemas.steep_infusion import SteepInfusionCreate, SteepInfusionRead


class SessionBase(BaseModel):
    tea_id: int
    teaware_id: int | None = None
    session_date: date
    steeps_count: int | None = None
    water_temp_c: float | None = None
    leaf_weight_g: float | None = None
    water_volume_ml: float | None = None
    brew_method: str | None = None
    rating: int | None = None
    notes: str | None = None

    @field_validator("session_date", mode="before")
    @classmethod
    def parse_session_date(cls, value: object) -> object:
        if isinstance(value, str):
            for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
                try:
                    from datetime import datetime
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
            raise ValueError(f"Invalid date format: {value!r}. Use DD/MM/YYYY or YYYY-MM-DD.")
        return value


class SessionCreate(SessionBase):
    steep_infusions: list[SteepInfusionCreate] = []


class SessionUpdate(SessionBase):
    steep_infusions: list[SteepInfusionCreate] = []


class SessionRead(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    steep_infusions: list[SteepInfusionRead] = []

    @field_serializer("session_date")
    def serialize_session_date(self, value: date) -> str:
        return value.strftime("%d/%m/%Y")
