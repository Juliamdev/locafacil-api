from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.casa_repository import CasaRepository
from app.schemas.casa import CasaCreate, CasaUpdate


class CasaService:
    def __init__(self, db: Session):
        self.repository = CasaRepository(db)

    def listar_casas(self):
        return self.repository.listar()

    def criar_casa(self, dados: CasaCreate):
        return self.repository.criar(dados)

    def atualizar_casa(self, casa_id, dados: CasaUpdate):
        casa = self.repository.buscar_por_id(casa_id)
        if not casa:
            raise HTTPException(status_code=404, detail="Casa não encontrada")
        return self.repository.atualizar(casa, dados)

    def excluir_casa(self, casa_id):
        casa = self.repository.buscar_por_id(casa_id)
        if not casa:
            raise HTTPException(status_code=404, detail="Casa não encontrada")
        if self.repository.tem_contrato_vinculado(casa_id):
            raise HTTPException(
                status_code=409,
                detail="Não é possível excluir: essa casa tem contratos vinculados.",
            )
        self.repository.excluir(casa)
