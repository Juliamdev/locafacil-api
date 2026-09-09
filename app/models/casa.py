import uuid
from sqlalchemy import Column, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Casa(Base):
    __tablename__ = "casas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    endereco = Column(String, nullable=False)
    valor_referencia = Column(Numeric(10, 2), nullable=False)

    contratos = relationship("Contrato", back_populates="casa")
