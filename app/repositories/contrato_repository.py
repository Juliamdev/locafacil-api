from sqlalchemy.orm import Session

from app.models.contrato import Contrato
from app.models.parcela import Parcela


class ContratoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Contrato]:
        return self.db.query(Contrato).all()

    def buscar_por_id(self, contrato_id) -> Contrato | None:
        return self.db.query(Contrato).filter(Contrato.id == contrato_id).first()

    def salvar(self, contrato: Contrato) -> Contrato:
        self.db.add(contrato)
        self.db.commit()
        self.db.refresh(contrato)
        return contrato

    def salvar_parcelas(self, parcelas: list[Parcela]) -> None:
        self.db.add_all(parcelas)
        self.db.commit()

    def listar_parcelas_em_aberto(self, contrato_id) -> list[Parcela]:
        """Parcelas com saldo > 0, da mais antiga para a mais recente —
        base para a alocação de pagamento (dívida mais antiga primeiro)."""
        return (
            self.db.query(Parcela)
            .filter(Parcela.contrato_id == contrato_id)
            .filter(Parcela.valor_pago < Parcela.valor_esperado)
            .order_by(Parcela.data_vencimento.asc())
            .all()
        )
