from pydantic import BaseModel, ConfigDict


class TeaBase(BaseModel):
    name: str
    vendor: str | None = None
    origin: str | None = None
    tea_type: str | None = None
    initial_quantity_g: float | None = None
    current_quantity_g: float | None = None
    harvest_year: int | None = None
    notes: str | None = None


class TeaCreate(TeaBase):
    pass


class TeaUpdate(TeaBase):
    pass


class TeaRead(TeaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TeaQuantityUpdate(BaseModel):
    current_quantity_g: float | None = None