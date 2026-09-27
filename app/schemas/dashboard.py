from pydantic import BaseModel


class DashboardKpisOut(BaseModel):
    total_previsto_mes: float
    total_recebido_mes: float
    taxa_inadimplencia: float  # percentual (0-100) de contratos ativos com parcela em atraso
    imoveis_ocupados: int
    imoveis_vagos: int
    imoveis_total: int
