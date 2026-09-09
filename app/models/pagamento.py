import uuid
from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Pagamento(Base):
    """Representa um recebimento real (ex: um Pix) — o evento financeiro em si.

    O valor recebido é distribuído entre uma ou mais Parcelas através de
    PagamentoParcela, sempre começando pela parcela em aberto mais antiga.
    """

    __tablename__ = "pagamentos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contrato_id = Column(UUID(as_uuid=True), ForeignKey("contratos.id"), nullable=False)

    data_pagamento = Column(Date, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    forma_pagamento = Column(String, nullable=False, default="pix")

    contrato = relationship("Contrato", back_populates="pagamentos")
    alocacoes = relationship("PagamentoParcela", back_populates="pagamento")


class PagamentoParcela(Base):
    """Tabela de alocação: registra quanto de um Pagamento foi aplicado a cada Parcela."""

    __tablename__ = "pagamento_parcelas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pagamento_id = Column(UUID(as_uuid=True), ForeignKey("pagamentos.id"), nullable=False)
    parcela_id = Column(UUID(as_uuid=True), ForeignKey("parcelas.id"), nullable=False)
    valor_alocado = Column(Numeric(10, 2), nullable=False)

    pagamento = relationship("Pagamento", back_populates="alocacoes")
    parcela = relationship("Parcela", back_populates="alocacoes")

    @property
    def mes_referencia(self):
        return self.parcela.mes_referencia
