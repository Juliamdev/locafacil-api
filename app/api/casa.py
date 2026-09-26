import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.casa import CasaCreate, CasaUpdate, CasaOut
from app.services.casa_service import CasaService

router = APIRouter(prefix="/casas", tags=["Casas"])


@router.get("/", response_model=list[CasaOut])
def listar_casas(db: Session = Depends(get_db)):
    return CasaService(db).listar_casas()


@router.post("/", response_model=CasaOut, status_code=201)
def criar_casa(dados: CasaCreate, db: Session = Depends(get_db)):
    return CasaService(db).criar_casa(dados)


@router.put("/{casa_id}", response_model=CasaOut)
def atualizar_casa(casa_id: uuid.UUID, dados: CasaUpdate, db: Session = Depends(get_db)):
    return CasaService(db).atualizar_casa(casa_id, dados)


@router.delete("/{casa_id}", status_code=204)
def excluir_casa(casa_id: uuid.UUID, db: Session = Depends(get_db)):
    CasaService(db).excluir_casa(casa_id)
