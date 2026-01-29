from datetime import datetime

from watchdog.routing.alertas.enums import RegrasEnum
from watchdog.routing.alertas.schemas import AlertaResponse
from watchdog.routing.alertas.service import AlertasService
from watchdog.routing.clientes.service import ClientesService
from watchdog.routing.clientes.schemas import ClienteResponse
from watchdog.routing.transacoes.enums import MoedaEnum
from watchdog.routing.transacoes.schemas import TransacaoResponse
from watchdog.routing.transacoes.service import TransacoesService
from watchdog.routing.relatorios.schemas import (
    AlertaRelatorio,
    AlertasInfo,
    RelatorioResponse,
    TransacaoRelatorio,
    TransacoesInfo
)


class RelatorioService:

    @classmethod
    async def get_report(
        cls,
        cliente_id: str,
        periodo_inicio: datetime | None,
        periodo_fim: datetime | None
    ) -> RelatorioResponse:
        """Get the report for the given cliente and period.

        Args:
            cliente_id (str): The cliente id.
            periodo_inicio (datetime | None): The start date.
            periodo_fim (datetime | None): The end date.

        Returns:
            RelatorioResponse: The final report.
        """
        cliente_info = await cls.get_cliente_info(cliente_id)
        transacoes_info = await cls.get_transacoes_info(
            cliente_id,
            periodo_inicio,
            periodo_fim
        )
        alertas_info = await cls.get_alertas_info(
            cliente_id,
            periodo_inicio,
            periodo_fim
        )
        return RelatorioResponse(
            cliente_id=cliente_info.id,
            nome=cliente_info.nome,
            email=cliente_info.email,
            pais=cliente_info.pais,
            nivel_risco=cliente_info.nivel_risco,
            status_kyc=cliente_info.status_kyc,
            transacoes_info=transacoes_info,
            alertas_info=alertas_info
        )

    @classmethod
    async def get_cliente_info(cls, cliente_id: str) -> ClienteResponse:
        """Get the cliente info.

        Args:
            cliente_id (str): The cliente id.

        Returns:
            ClienteResponse: The cliente info.
        """
        return await ClientesService.get_cliente_by_id(cliente_id)

    @classmethod
    async def get_transacoes_info(
        cls,
        cliente_id: str,
        periodo_inicio: datetime | None,
        periodo_fim: datetime | None
    ) -> TransacoesInfo:
        """Get the transacoes info for the given cliente and period.

        Args:
            cliente_id (str): The cliente id.
            periodo_inicio (datetime | None): The start date.
            periodo_fim (datetime | None): The end date.

        Returns:
            TransacoesInfo: The transacoes info.
        """
        rows = await TransacoesService.get_filtered_transactions(
            cliente_id=cliente_id,
            moeda=None,
            tipo=None,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim
        )

        numero_transacoes = len(rows)
        transacoes = []
        valores = {
            MoedaEnum.USD.value: 0,
            MoedaEnum.EUR.value: 0,
            MoedaEnum.BRL.value: 0
        }

        for row in rows:
            valores[row.moeda] += row.valor
            transacoes.append(await cls.__get_transacao_relatorio(row))

        return TransacoesInfo(
            numero_transacoes=numero_transacoes,
            transacoes=transacoes,
            valor_usd=valores.get(MoedaEnum.USD.value),
            valor_eur=valores.get(MoedaEnum.EUR.value),
            valor_brl=valores.get(MoedaEnum.BRL.value)
        )
    
    @classmethod
    async def get_alertas_info(
        cls,
        cliente_id: str,
        periodo_inicio: datetime | None,
        periodo_fim: datetime | None
    ) -> AlertasInfo:
        """Get the alertas info for the given cliente and period.

        Args:
            cliente_id (str): The cliente id.
            periodo_inicio (datetime | None): The start date.
            periodo_fim (datetime | None): The end date.

        Returns:
            AlertasInfo: The alertas info.
        """
        rows = await AlertasService.get_filtered_alertas(
            cliente_id=cliente_id,
            regra=None,
            severidade=None,
            status=None,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim
        )

        numero_alertas = len(rows)
        alertas = []
        regras_qtd = {
            RegrasEnum.LIMITE_DIARIO.value: 0,
            RegrasEnum.TRANSACOES_REPETIDAS.value: 0,
            RegrasEnum.PAISES_SUSPEITOS.value: 0
        }

        for row in rows:
            regras_qtd[row.regra] += 1
            alertas.append(await cls.__get_alerta_relatorio(row))

        return AlertasInfo(
            numero_alertas=numero_alertas,
            alertas=alertas,
            limite_diario=regras_qtd.get(RegrasEnum.LIMITE_DIARIO.value),
            fracionamento=regras_qtd.get(RegrasEnum.TRANSACOES_REPETIDAS.value),
            paises_suspeitos=regras_qtd.get(RegrasEnum.PAISES_SUSPEITOS.value)
        )

    @classmethod
    async def __get_transacao_relatorio(
        cls,
        transacao: TransacaoResponse
    ) -> TransacaoRelatorio:
        """Convert TransacaoResponse to TransacaoRelatorio

        Args:
            transacao (TransacaoResponse): Transacao to be converted.

        Returns:
            TransacaoRelatorio: The transacao converted for the report.
        """
        dump = transacao.model_dump()
        del dump["cliente_id"]
        return TransacaoRelatorio(**dump)

    @classmethod
    async def __get_alerta_relatorio(
        cls,
        alerta: AlertaResponse
    ) -> AlertaRelatorio:
        """Convert AlertaResponse to AlertaRelatorio

        Args:
            alerta (AlertaResponse): Alerta to be converted.

        Returns:
            AlertaRelatorio: The alerta converted for the report.
        """
        dump = alerta.model_dump()
        del dump["cliente_id"]
        return AlertaRelatorio(**dump)
