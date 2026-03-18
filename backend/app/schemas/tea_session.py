from datetime import datetime, timezone

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    field_serializer,
    field_validator,
)


class SessionBase(BaseModel):
    tea_id: int
    session_date: AwareDatetime
    steeps_count: int | None = None
    rating: int | None = None
    notes: str | None = None

    @field_validator("session_date")
    @classmethod
    def normalize_session_date(cls, value: datetime) -> datetime:
        return value.astimezone(timezone.utc)


class SessionCreate(SessionBase):
    pass


class SessionUpdate(SessionBase):
    pass


class SessionRead(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    @field_serializer("session_date")
    def serialize_session_date(self, value: datetime) -> str:
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
