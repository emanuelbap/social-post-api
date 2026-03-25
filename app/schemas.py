from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    mensagem: str = Field(min_length=1, max_length=5000)


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    titulo: str
    mensagem: str
    data: datetime
    usuario: str