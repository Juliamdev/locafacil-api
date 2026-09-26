from sqlalchemy.orm import Session

from app.models.inquilino import Inquilino
from app.models.contrato import Contrato
from app.schemas.inquilino import InquilinoCreate, InquilinoUpdate


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

    def atualizar(self, inquilino: Inquilino, dados: InquilinoUpdate) -> Inquilino:
        inquilino.nome = dados.nome
        inquilino.email = dados.email
        inquilino.telefone = dados.telefone
        self.db.add(inquilino)
        self.db.commit()
        self.db.refresh(inquilino)
        return inquilino

    def excluir(self, inquilino: Inquilino) -> None:
        self.db.delete(inquilino)
        self.db.commit()

    def tem_contrato_vinculado(self, inquilino_id) -> bool:
        return (
            self.db.query(Contrato).filter(Contrato.inquilino_id == inquilino_id).first()
            is not None
        )
