from sqlalchemy.orm import Session, joinedload

from app.models.pagamento import Pagamento, PagamentoParcela
from app.models.parcela import Parcela


class PagamentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar_pagamento(self, pagamento: Pagamento) -> Pagamento:
        self.db.add(pagamento)
        self.db.commit()
        self.db.refresh(pagamento)
        return pagamento

    def salvar_alocacoes(self, alocacoes: list[PagamentoParcela]) -> None:
        self.db.add_all(alocacoes)
        self.db.commit()

    def atualizar_parcela(self, parcela: Parcela) -> None:
        self.db.add(parcela)
        self.db.commit()

    def listar_parcelas_do_contrato(self, contrato_id) -> list[Parcela]:
        return (
            self.db.query(Parcela)
            .filter(Parcela.contrato_id == contrato_id)
            .order_by(Parcela.data_vencimento.asc())
            .all()
        )

    def listar_pagamentos_do_contrato(self, contrato_id) -> list[Pagamento]:
        """Histórico de pagamentos, mais recente primeiro, com as alocações
        já carregadas (evita N+1 queries ao serializar mes_referencia)."""
        return (
            self.db.query(Pagamento)
            .filter(Pagamento.contrato_id == contrato_id)
            .options(joinedload(Pagamento.alocacoes).joinedload(PagamentoParcela.parcela))
            .order_by(Pagamento.data_pagamento.desc())
            .all()
        )
