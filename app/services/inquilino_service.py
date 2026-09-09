from sqlalchemy.orm import Session

from app.repositories.inquilino_repository import InquilinoRepository
from app.schemas.inquilino import InquilinoCreate


class InquilinoService:
    def __init__(self, db: Session):
        self.repository = InquilinoRepository(db)

    def listar_inquilinos(self):
        return self.repository.listar()

    def criar_inquilino(self, dados: InquilinoCreate):
        return self.repository.criar(dados)
