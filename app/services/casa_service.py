from sqlalchemy.orm import Session

from app.repositories.casa_repository import CasaRepository
from app.schemas.casa import CasaCreate


class CasaService:
    """Camada de regra de negócio. Para Casa a regra é simples hoje (CRUD direto),
    mas fica aqui reservado o lugar para validações futuras (ex: impedir excluir
    uma casa com contrato ativo)."""

    def __init__(self, db: Session):
        self.repository = CasaRepository(db)

    def listar_casas(self):
        return self.repository.listar()

    def criar_casa(self, dados: CasaCreate):
        return self.repository.criar(dados)
