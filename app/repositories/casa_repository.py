from sqlalchemy.orm import Session

from app.models.casa import Casa
from app.models.contrato import Contrato
from app.schemas.casa import CasaCreate, CasaUpdate


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

    def atualizar(self, casa: Casa, dados: CasaUpdate) -> Casa:
        casa.endereco = dados.endereco
        self.db.add(casa)
        self.db.commit()
        self.db.refresh(casa)
        return casa

    def excluir(self, casa: Casa) -> None:
        self.db.delete(casa)
        self.db.commit()

    def tem_contrato_vinculado(self, casa_id) -> bool:
        return self.db.query(Contrato).filter(Contrato.casa_id == casa_id).first() is not None
