import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.inquilino import InquilinoCreate, InquilinoUpdate, InquilinoOut
from app.services.inquilino_service import InquilinoService

router = APIRouter(prefix="/inquilinos", tags=["Inquilinos"])


@router.get("/", response_model=list[InquilinoOut])
def listar_inquilinos(db: Session = Depends(get_db)):
    return InquilinoService(db).listar_inquilinos()


@router.post("/", response_model=InquilinoOut, status_code=201)
def criar_inquilino(dados: InquilinoCreate, db: Session = Depends(get_db)):
    return InquilinoService(db).criar_inquilino(dados)


@router.put("/{inquilino_id}", response_model=InquilinoOut)
def atualizar_inquilino(inquilino_id: uuid.UUID, dados: InquilinoUpdate, db: Session = Depends(get_db)):
    return InquilinoService(db).atualizar_inquilino(inquilino_id, dados)


@router.delete("/{inquilino_id}", status_code=204)
def excluir_inquilino(inquilino_id: uuid.UUID, db: Session = Depends(get_db)):
    InquilinoService(db).excluir_inquilino(inquilino_id)
