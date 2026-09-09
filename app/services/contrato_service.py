import calendar
from datetime import date

from sqlalchemy.orm import Session
from dateutil.relativedelta import relativedelta

from app.models.contrato import Contrato, StatusContrato
from app.models.parcela import Parcela
from app.repositories.contrato_repository import ContratoRepository
from app.schemas.contrato import ContratoCreate, ContratoEncerrar


class ContratoService:
    def __init__(self, db: Session):
        self.repository = ContratoRepository(db)

    def listar_contratos(self):
        return self.repository.listar()

    def criar_contrato(self, dados: ContratoCreate) -> Contrato:
        data_fim_prevista = dados.data_inicio + relativedelta(years=1)

        contrato = Contrato(
            casa_id=dados.casa_id,
            inquilino_id=dados.inquilino_id,
            valor_aluguel=dados.valor_aluguel,
            dia_vencimento=dados.dia_vencimento,
            data_inicio=dados.data_inicio,
            data_fim_prevista=data_fim_prevista,
            status=StatusContrato.ATIVO,
        )
        contrato = self.repository.salvar(contrato)

        parcelas = self._gerar_parcelas_do_ano(contrato)
        self.repository.salvar_parcelas(parcelas)

        return contrato

    def encerrar_contrato(self, contrato_id, dados: ContratoEncerrar) -> Contrato:
        """RF04: contrato pode ser encerrado antes do prazo previsto
        (saída do inquilino ou pedido do proprietário)."""
        contrato = self.repository.buscar_por_id(contrato_id)
        contrato.status = StatusContrato.ENCERRADO
        contrato.data_fim_real = dados.data_fim_real
        return self.repository.salvar(contrato)

    def _gerar_parcelas_do_ano(self, contrato: Contrato) -> list[Parcela]:
        """Gera as 12 parcelas mensais do contrato, respeitando o dia de
        vencimento e ajustando para meses mais curtos (ex: dia 31 em fevereiro
        vira o último dia do mês)."""
        parcelas = []
        for i in range(12):
            mes_ref = contrato.data_inicio + relativedelta(months=i)
            ultimo_dia_do_mes = calendar.monthrange(mes_ref.year, mes_ref.month)[1]
            dia = min(contrato.dia_vencimento, ultimo_dia_do_mes)
            data_vencimento = date(mes_ref.year, mes_ref.month, dia)

            parcelas.append(
                Parcela(
                    contrato_id=contrato.id,
                    mes_referencia=f"{mes_ref.year}-{mes_ref.month:02d}",
                    data_vencimento=data_vencimento,
                    valor_esperado=contrato.valor_aluguel,
                    valor_pago=0,
                )
            )
        return parcelas
