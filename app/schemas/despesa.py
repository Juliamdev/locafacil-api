import uuid
from datetime import date
from pydantic import BaseModel


class DespesaCreate(BaseModel):
    casa_id: uuid.UUID
    descricao: str
    valor: float
    data: date


class DespesaOut(BaseModel):
    id: uuid.UUID
    casa_id: uuid.UUID
    descricao: str
    valor: float
    data: date

    class Config:
        from_attributes = True
