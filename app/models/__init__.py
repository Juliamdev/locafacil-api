from app.models.casa import Casa
from app.models.inquilino import Inquilino
from app.models.contrato import Contrato, StatusContrato
from app.models.parcela import Parcela
from app.models.pagamento import Pagamento, PagamentoParcela

__all__ = [
    "Casa",
    "Inquilino",
    "Contrato",
    "StatusContrato",
    "Parcela",
    "Pagamento",
    "PagamentoParcela",
]
