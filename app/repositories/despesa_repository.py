from sqlalchemy.orm import Session

from app.models.despesa import Despesa
from app.schemas.despesa import DespesaCreate


class DespesaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_por_casa(self, casa_id) -> list[Despesa]:
        return (
            self.db.query(Despesa)
            .filter(Despesa.casa_id == casa_id)
            .order_by(Despesa.data.desc())
            .all()
        )

    def buscar_por_id(self, despesa_id) -> Despesa | None:
        return self.db.query(Despesa).filter(Despesa.id == despesa_id).first()

    def criar(self, dados: DespesaCreate) -> Despesa:
        despesa = Despesa(**dados.model_dump())
        self.db.add(despesa)
        self.db.commit()
        self.db.refresh(despesa)
        return despesa

    def excluir(self, despesa: Despesa) -> None:
        self.db.delete(despesa)
        self.db.commit()
