import uuid
from datetime import date
from pydantic import BaseModel

from app.models.contrato import StatusContrato


class ContratoCreate(BaseModel):
    casa_id: uuid.UUID
    inquilino_id: uuid.UUID
    valor_aluguel: float
    dia_vencimento: int
    data_inicio: date


class ContratoEncerrar(BaseModel):
    data_fim_real: date


class ContratoOut(BaseModel):
    id: uuid.UUID
    casa_id: uuid.UUID
    inquilino_id: uuid.UUID
    valor_aluguel: float
    dia_vencimento: int
    data_inicio: date
    data_fim_prevista: date
    data_fim_real: date | None
    status: StatusContrato

    class Config:
        from_attributes = True
