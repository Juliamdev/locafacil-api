from sqlalchemy.orm import Session

from app.models.inquilino import Inquilino
from app.schemas.inquilino import InquilinoCreate


class InquilinoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Inquilino]:
        return self.db.query(Inquilino).all()

    def buscar_por_id(self, inquilino_id) -> Inquilino | None:
        return self.db.query(Inquilino).filter(Inquilino.id == inquilino_id).first()

    def criar(self, dados: InquilinoCreate) -> Inquilino:
        inquilino = Inquilino(**dados.model_dump())
        self.db.add(inquilino)
        self.db.commit()
        self.db.refresh(inquilino)
        return inquilino
