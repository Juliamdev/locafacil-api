import uuid
from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Parcela(Base):
    """Representa a cobrança de um mês de referência de um contrato.

    valor_pago é atualizado conforme pagamentos vão sendo alocados a ela
    (ver PagamentoParcela) — não representa um pagamento em si.
    """

    __tablename__ = "parcelas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contrato_id = Column(UUID(as_uuid=True), ForeignKey("contratos.id"), nullable=False)

    mes_referencia = Column(String, nullable=False)  # formato "YYYY-MM"
    data_vencimento = Column(Date, nullable=False)

    valor_esperado = Column(Numeric(10, 2), nullable=False)
    valor_pago = Column(Numeric(10, 2), nullable=False, default=0)

    contrato = relationship("Contrato", back_populates="parcelas")
    alocacoes = relationship("PagamentoParcela", back_populates="parcela")

    @property
    def saldo(self):
        return self.valor_esperado - self.valor_pago
