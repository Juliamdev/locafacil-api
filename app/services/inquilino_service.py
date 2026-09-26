from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.inquilino_repository import InquilinoRepository
from app.schemas.inquilino import InquilinoCreate, InquilinoUpdate


class InquilinoService:
    def __init__(self, db: Session):
        self.repository = InquilinoRepository(db)

    def listar_inquilinos(self):
        return self.repository.listar()

    def criar_inquilino(self, dados: InquilinoCreate):
        return self.repository.criar(dados)

    def atualizar_inquilino(self, inquilino_id, dados: InquilinoUpdate):
        inquilino = self.repository.buscar_por_id(inquilino_id)
        if not inquilino:
            raise HTTPException(status_code=404, detail="Inquilino não encontrado")
        return self.repository.atualizar(inquilino, dados)

    def excluir_inquilino(self, inquilino_id):
        inquilino = self.repository.buscar_por_id(inquilino_id)
        if not inquilino:
            raise HTTPException(status_code=404, detail="Inquilino não encontrado")
        if self.repository.tem_contrato_vinculado(inquilino_id):
            raise HTTPException(
                status_code=409,
                detail="Não é possível excluir: esse inquilino tem contratos vinculados.",
            )
        self.repository.excluir(inquilino)
