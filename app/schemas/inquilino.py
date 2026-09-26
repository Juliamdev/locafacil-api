import uuid
from pydantic import BaseModel, EmailStr


class InquilinoBase(BaseModel):
    nome: str
    email: EmailStr | None = None
    telefone: str | None = None


class InquilinoCreate(InquilinoBase):
    pass


class InquilinoUpdate(InquilinoBase):
    pass


class InquilinoOut(InquilinoBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
