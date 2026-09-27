import uuid
from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Despesa(Base):
    """Custo lançado numa casa (manutenção, IPTU, etc), usado para calcular
    o rendimento líquido real do proprietário — não afeta o cálculo de
    saldo devedor de aluguel, que continua exclusivo de Contrato/Parcela."""

    __tablename__ = "despesas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    casa_id = Column(UUID(as_uuid=True), ForeignKey("casas.id"), nullable=False)
    descricao = Column(String, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    data = Column(Date, nullable=False)

    casa = relationship("Casa", back_populates="despesas")
