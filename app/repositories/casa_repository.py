from sqlalchemy.orm import Session

from app.models.casa import Casa
from app.schemas.casa import CasaCreate


class CasaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Casa]:
        return self.db.query(Casa).all()

    def buscar_por_id(self, casa_id) -> Casa | None:
        return self.db.query(Casa).filter(Casa.id == casa_id).first()

    def criar(self, dados: CasaCreate) -> Casa:
        casa = Casa(**dados.model_dump())
        self.db.add(casa)
        self.db.commit()
        self.db.refresh(casa)
        return casa
