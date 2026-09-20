from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.pagamento import Pagamento, PagamentoParcela
from app.repositories.contrato_repository import ContratoRepository
from app.repositories.pagamento_repository import PagamentoRepository
from app.schemas.pagamento import PagamentoCreate, ContratoStatusOut


class PagamentoService:
    def __init__(self, db: Session):
        self.pagamento_repo = PagamentoRepository(db)
        self.contrato_repo = ContratoRepository(db)

    def registrar_pagamento(self, dados: PagamentoCreate) -> Pagamento:
        """Registra o recebimento e distribui o valor entre as parcelas em
        aberto, sempre da mais antiga para a mais recente (regra definida:
        pagamento parcial abate a dívida mais antiga primeiro, já que é via
        Pix e não vinculado a um boleto específico)."""

        pagamento = Pagamento(
            contrato_id=dados.contrato_id,
            data_pagamento=dados.data_pagamento,
            valor=dados.valor,
            forma_pagamento=dados.forma_pagamento,
        )
        pagamento = self.pagamento_repo.salvar_pagamento(pagamento)

        valor_restante = Decimal(str(dados.valor))
        parcelas_abertas = self.contrato_repo.listar_parcelas_em_aberto(dados.contrato_id)

        alocacoes = []
        for parcela in parcelas_abertas:
            if valor_restante <= 0:
                break

            valor_alocado = min(valor_restante, parcela.saldo)
            parcela.valor_pago += valor_alocado
            self.pagamento_repo.atualizar_parcela(parcela)

            alocacoes.append(
                PagamentoParcela(
                    pagamento_id=pagamento.id,
                    parcela_id=parcela.id,
                    valor_alocado=valor_alocado,
                )
            )
            valor_restante -= valor_alocado

        # Se sobrar valor além de todas as parcelas em aberto (ex: adiantamento),
        # ele fica sem alocação por ora — cenário para tratar quando surgir na prática.
        self.pagamento_repo.salvar_alocacoes(alocacoes)

        return pagamento

    def status_do_contrato(self, contrato_id) -> ContratoStatusOut:
        """Calcula saldo devedor acumulado e status (em_dia / parcial / atrasado).

        - atrasado: existe parcela com saldo em aberto cujo vencimento já passou
          (a partir do dia seguinte, sem tolerância)
        - parcial: há saldo devedor, mas nenhuma parcela vencida (ex: mês atual
          pago parcialmente antes do vencimento)
        - em_dia: saldo devedor igual a zero
        """
        parcelas = self.pagamento_repo.listar_parcelas_do_contrato(contrato_id)
        hoje = date.today()

        # Só parcelas já vencidas (ou vencendo hoje) contam como exigíveis —
        # parcelas futuras ainda não são dívida, mesmo que não pagas.
        parcelas_exigiveis = [p for p in parcelas if p.data_vencimento <= hoje]

        saldo_devedor = sum((p.saldo for p in parcelas_exigiveis), Decimal("0"))
        tem_parcela_atrasada = any(p.saldo > 0 and p.data_vencimento < hoje for p in parcelas_exigiveis)

        if tem_parcela_atrasada:
            status = "atrasado"
        elif saldo_devedor > 0:
            status = "parcial"
        else:
            status = "em_dia"

        return ContratoStatusOut(
            contrato_id=contrato_id,
            saldo_devedor=float(saldo_devedor),
            status=status,
        )

    def historico_de_pagamentos(self, contrato_id):
        return self.pagamento_repo.listar_pagamentos_do_contrato(contrato_id)
