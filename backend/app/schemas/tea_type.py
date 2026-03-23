from pydantic import BaseModel, ConfigDict


class TeaTypeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    category: str


class TeaTypeRead(TeaTypeBase):
    pass


class TeaTypeCreate(TeaTypeBase):
    pass


class TeaTypeUpdate(TeaTypeBase):
    pass
