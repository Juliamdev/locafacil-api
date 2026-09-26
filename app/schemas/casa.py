import uuid
from pydantic import BaseModel


class CasaBase(BaseModel):
    endereco: str


class CasaCreate(CasaBase):
    pass


class CasaUpdate(CasaBase):
    pass


class CasaOut(CasaBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
