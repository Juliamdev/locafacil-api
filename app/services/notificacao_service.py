from datetime import date, timedelta

from sqlalchemy.orm import Session, joinedload

from app.database import settings
from app.models.contrato import Contrato, StatusContrato
from app.models.parcela import Parcela


class NotificacaoService:
    """Monta o resumo diário de contratos que precisam de atenção:
    vencimento próximo (dentro da janela configurada) ou saldo devedor em aberto.
    """

    def __init__(self, db: Session):
        self.db = db

    def gerar_resumo(self) -> list[dict]:
        hoje = date.today()
        limite_alerta = hoje + timedelta(days=settings.dias_antecedencia_alerta)

        contratos_ativos = (
            self.db.query(Contrato)
            .options(joinedload(Contrato.casa), joinedload(Contrato.inquilino))
            .filter(Contrato.status == StatusContrato.ATIVO)
            .all()
        )

        itens = []
        for contrato in contratos_ativos:
            parcelas_abertas = (
                self.db.query(Parcela)
                .filter(Parcela.contrato_id == contrato.id)
                .filter(Parcela.valor_pago < Parcela.valor_esperado)
                .order_by(Parcela.data_vencimento.asc())
                .all()
            )
            if not parcelas_abertas:
                continue  # contrato em dia, nada a alertar

            proxima = parcelas_abertas[0]
            saldo_devedor = sum(
                (p.saldo for p in parcelas_abertas if p.data_vencimento <= hoje),
                start=type(proxima.saldo)(0),
            )
            atrasado = proxima.data_vencimento < hoje
            venc_proximo = hoje <= proxima.data_vencimento <= limite_alerta

            if not (atrasado or venc_proximo or saldo_devedor > 0):
                continue

            itens.append(
                {
                    "casa_endereco": contrato.casa.endereco,
                    "inquilino_nome": contrato.inquilino.nome,
                    "proxima_data_vencimento": proxima.data_vencimento,
                    "atrasado": atrasado,
                    "saldo_devedor": float(saldo_devedor),
                }
            )

        return itens

    def montar_corpo_email(self, itens: list[dict]) -> str:
        if not itens:
            return "<p>Nenhum contrato com vencimento próximo ou pendência hoje.</p>"

        linhas = []
        for item in itens:
            situacao = "ATRASADO" if item["atrasado"] else "vencimento próximo"
            linhas.append(
                f"<li><b>{item['casa_endereco']}</b> — {item['inquilino_nome']}: "
                f"{situacao}, vence em {item['proxima_data_vencimento']}, "
                f"saldo devedor R$ {item['saldo_devedor']:.2f}</li>"
            )

        return f"<p>Resumo do dia:</p><ul>{''.join(linhas)}</ul>"
