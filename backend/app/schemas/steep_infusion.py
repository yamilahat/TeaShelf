from pydantic import BaseModel, ConfigDict


class SteepInfusionBase(BaseModel):
    steep_number: int
    steep_time_seconds: int


class SteepInfusionCreate(SteepInfusionBase):
    pass


class SteepInfusionRead(SteepInfusionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
