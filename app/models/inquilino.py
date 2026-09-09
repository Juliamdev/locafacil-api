import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Inquilino(Base):
    __tablename__ = "inquilinos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=True)
    telefone = Column(String, nullable=True)

    contratos = relationship("Contrato", back_populates="inquilino")
