import uuid
from datetime import date
from pydantic import BaseModel


class PagamentoCreate(BaseModel):
    contrato_id: uuid.UUID
    data_pagamento: date
    valor: float
    forma_pagamento: str = "pix"


class AlocacaoOut(BaseModel):
    parcela_id: uuid.UUID
    mes_referencia: str
    valor_alocado: float


class PagamentoOut(BaseModel):
    id: uuid.UUID
    contrato_id: uuid.UUID
    data_pagamento: date
    valor: float
    forma_pagamento: str
    alocacoes: list[AlocacaoOut]

    class Config:
        from_attributes = True


class ContratoStatusOut(BaseModel):
    contrato_id: uuid.UUID
    saldo_devedor: float
    status: str  # "em_dia" | "parcial" | "atrasado"
