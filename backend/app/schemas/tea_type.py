from pydantic import BaseModel, ConfigDict


class TeaTypeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
