import uuid
import enum
from sqlalchemy import Column, String, Numeric, Integer, Date, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class StatusContrato(str, enum.Enum):
    ATIVO = "ativo"
    ENCERRADO = "encerrado"


class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    casa_id = Column(UUID(as_uuid=True), ForeignKey("casas.id"), nullable=False)
    inquilino_id = Column(UUID(as_uuid=True), ForeignKey("inquilinos.id"), nullable=False)

    valor_aluguel = Column(Numeric(10, 2), nullable=False)
    dia_vencimento = Column(Integer, nullable=False)  # dia do mês, ex: 5, 10, 15

    data_inicio = Column(Date, nullable=False)
    data_fim_prevista = Column(Date, nullable=False)  # data_inicio + 1 ano
    data_fim_real = Column(Date, nullable=True)  # preenchida se encerrado antecipadamente

    status = Column(Enum(StatusContrato), nullable=False, default=StatusContrato.ATIVO)

    casa = relationship("Casa", back_populates="contratos")
    inquilino = relationship("Inquilino", back_populates="contratos")
    parcelas = relationship("Parcela", back_populates="contrato")
    pagamentos = relationship("Pagamento", back_populates="contrato")
