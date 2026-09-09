import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.contrato import ContratoCreate, ContratoOut, ContratoEncerrar
from app.services.contrato_service import ContratoService

router = APIRouter(prefix="/contratos", tags=["Contratos"])


@router.get("/", response_model=list[ContratoOut])
def listar_contratos(db: Session = Depends(get_db)):
    return ContratoService(db).listar_contratos()


@router.post("/", response_model=ContratoOut, status_code=201)
def criar_contrato(dados: ContratoCreate, db: Session = Depends(get_db)):
    """Cria o contrato de 1 ano e já gera as 12 parcelas mensais."""
    return ContratoService(db).criar_contrato(dados)


@router.patch("/{contrato_id}/encerrar", response_model=ContratoOut)
def encerrar_contrato(contrato_id: uuid.UUID, dados: ContratoEncerrar, db: Session = Depends(get_db)):
    """RF04: encerramento antecipado (saída do inquilino ou pedido do proprietário)."""
    return ContratoService(db).encerrar_contrato(contrato_id, dados)
