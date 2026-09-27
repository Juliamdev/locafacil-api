from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.despesa_repository import DespesaRepository
from app.schemas.despesa import DespesaCreate


class DespesaService:
    def __init__(self, db: Session):
        self.repository = DespesaRepository(db)

    def listar_por_casa(self, casa_id):
        return self.repository.listar_por_casa(casa_id)

    def criar_despesa(self, dados: DespesaCreate):
        return self.repository.criar(dados)

    def excluir_despesa(self, despesa_id):
        despesa = self.repository.buscar_por_id(despesa_id)
        if not despesa:
            raise HTTPException(status_code=404, detail="Despesa não encontrada")
        self.repository.excluir(despesa)
