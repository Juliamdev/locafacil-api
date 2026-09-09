import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.pagamento import PagamentoCreate, PagamentoOut, ContratoStatusOut
from app.services.pagamento_service import PagamentoService

router = APIRouter(tags=["Pagamentos"])


@router.post("/pagamentos/", response_model=PagamentoOut, status_code=201)
def registrar_pagamento(dados: PagamentoCreate, db: Session = Depends(get_db)):
    """Registra um pagamento (pode ser parcial) e aloca o valor às parcelas
    em aberto mais antigas primeiro."""
    return PagamentoService(db).registrar_pagamento(dados)


@router.get("/contratos/{contrato_id}/status", response_model=ContratoStatusOut)
def status_do_contrato(contrato_id: uuid.UUID, db: Session = Depends(get_db)):
    """Retorna o saldo devedor acumulado e o status (em_dia/parcial/atrasado)."""
    return PagamentoService(db).status_do_contrato(contrato_id)
