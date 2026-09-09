from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.inquilino import InquilinoCreate, InquilinoOut
from app.services.inquilino_service import InquilinoService

router = APIRouter(prefix="/inquilinos", tags=["Inquilinos"])


@router.get("/", response_model=list[InquilinoOut])
def listar_inquilinos(db: Session = Depends(get_db)):
    return InquilinoService(db).listar_inquilinos()


@router.post("/", response_model=InquilinoOut, status_code=201)
def criar_inquilino(dados: InquilinoCreate, db: Session = Depends(get_db)):
    return InquilinoService(db).criar_inquilino(dados)
