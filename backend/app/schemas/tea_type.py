from pydantic import BaseModel, ConfigDict


class TeaTypeBase(BaseModel):
    name: str
    category: str


class TeaTypeRead(TeaTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TeaTypeCreate(TeaTypeBase):
    pass


class TeaTypeUpdate(TeaTypeBase):
    pass
