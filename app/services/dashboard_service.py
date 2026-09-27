from datetime import date

from sqlalchemy.orm import Session

from app.models.casa import Casa
from app.models.contrato import Contrato, StatusContrato
from app.models.parcela import Parcela
from app.schemas.dashboard import DashboardKpisOut


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def calcular_kpis(self) -> DashboardKpisOut:
        hoje = date.today()
        mes_atual = f"{hoje.year}-{hoje.month:02d}"

        contratos_ativos = (
            self.db.query(Contrato).filter(Contrato.status == StatusContrato.ATIVO).all()
        )
        ids_contratos_ativos = [c.id for c in contratos_ativos]

        # Previsto x recebido do mês corrente: olha só as parcelas cujo mês
        # de referência é o mês atual, dos contratos ativos.
        total_previsto_mes = 0.0
        total_recebido_mes = 0.0
        if ids_contratos_ativos:
            parcelas_do_mes = (
                self.db.query(Parcela)
                .filter(Parcela.contrato_id.in_(ids_contratos_ativos))
                .filter(Parcela.mes_referencia == mes_atual)
                .all()
            )
            total_previsto_mes = float(sum(p.valor_esperado for p in parcelas_do_mes))
            total_recebido_mes = float(sum(p.valor_pago for p in parcelas_do_mes))

        # Inadimplência: contratos ativos com ao menos uma parcela vencida
        # (venceu antes de hoje) e ainda com saldo em aberto.
        contratos_inadimplentes = 0
        if ids_contratos_ativos:
            parcelas_de_todos = (
                self.db.query(Parcela)
                .filter(Parcela.contrato_id.in_(ids_contratos_ativos))
                .all()
            )
            por_contrato: dict = {}
            for p in parcelas_de_todos:
                por_contrato.setdefault(p.contrato_id, []).append(p)

            for parcelas in por_contrato.values():
                if any(p.saldo > 0 and p.data_vencimento < hoje for p in parcelas):
                    contratos_inadimplentes += 1

        taxa_inadimplencia = (
            (contratos_inadimplentes / len(contratos_ativos)) * 100 if contratos_ativos else 0.0
        )

        # Ocupação: casa é considerada ocupada se tem ao menos um contrato ativo.
        casas_total = self.db.query(Casa).count()
        casas_ocupadas = len({c.casa_id for c in contratos_ativos})
        casas_vagas = casas_total - casas_ocupadas

        return DashboardKpisOut(
            total_previsto_mes=total_previsto_mes,
            total_recebido_mes=total_recebido_mes,
            taxa_inadimplencia=round(taxa_inadimplencia, 1),
            imoveis_ocupados=casas_ocupadas,
            imoveis_vagos=casas_vagas,
            imoveis_total=casas_total,
        )
