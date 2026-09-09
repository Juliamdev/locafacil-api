import uuid
from pydantic import BaseModel


class CasaBase(BaseModel):
    endereco: str
    valor_referencia: float


class CasaCreate(CasaBase):
    pass


class CasaOut(CasaBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
