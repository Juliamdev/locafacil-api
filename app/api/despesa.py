import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.despesa import DespesaCreate, DespesaOut
from app.services.despesa_service import DespesaService

router = APIRouter(tags=["Despesas"])


@router.get("/casas/{casa_id}/despesas", response_model=list[DespesaOut])
def listar_despesas_da_casa(casa_id: uuid.UUID, db: Session = Depends(get_db)):
    return DespesaService(db).listar_por_casa(casa_id)


@router.post("/despesas/", response_model=DespesaOut, status_code=201)
def criar_despesa(dados: DespesaCreate, db: Session = Depends(get_db)):
    return DespesaService(db).criar_despesa(dados)


@router.delete("/despesas/{despesa_id}", status_code=204)
def excluir_despesa(despesa_id: uuid.UUID, db: Session = Depends(get_db)):
    DespesaService(db).excluir_despesa(despesa_id)
