from uuid import uuid4
from datetime import datetime, time

from watchdog.database.database import Database
from watchdog.database.entities import transacoes_table
from watchdog.compliance.service import ComplianceService
from watchdog.routing.alertas.enums import (
    StatusEnum,
    SEVERIDADE_ENUM_MAP
)
from watchdog.routing.alertas.schemas import AlertaRequest
from watchdog.routing.alertas.service import AlertasService
from watchdog.routing.transacoes.enums import TipoTransacaoEnum, MoedaEnum
from watchdog.routing.transacoes.exceptions import TransactionNotFoundException
from watchdog.routing.transacoes.schemas import (
    TransancaoRequest,
    TransacaoResponse
)

class TransacoesService:

    @classmethod
    async def create(cls, new_transacao: TransancaoRequest) -> TransacaoResponse:
        """Create a new transaction in the database.
        
        Args:
            new_transacao (TransancaoRequest): The transaction data to be created.

        Returns:
            TransacaoResponse: The created transaction data.
        """
        new_id = uuid4()
        date_created = datetime.now()

        query = transacoes_table.insert().values(
            id = new_id,
            cliente_id = new_transacao.cliente_id,
            tipo = new_transacao.tipo.value,
            valor = new_transacao.valor,
            moeda = new_transacao.moeda.value,
            contraparte = new_transacao.contraparte,
            data_hora = date_created
        )
        query_list = await cls.get_alertas_querys(
            transacao_id=str(new_id),
            cliente_id=new_transacao.cliente_id,
            contraparte=new_transacao.contraparte,
            valor=new_transacao.valor,
            moeda=new_transacao.moeda
        )
        query_list.insert(0, query)

        await Database.execute_many(query_list)
        return TransacaoResponse(id=new_id, **new_transacao.model_dump(), data_hora=date_created)

    @classmethod
    async def get_alertas_querys(
        cls,
        transacao_id: str,
        cliente_id: str,
        contraparte: str | None,
        valor: float,
        moeda: MoedaEnum
    ) -> list:
        """Generate alert queries based on transaction data.

        Args:
            transacao_id (str): The ID of the transaction.
            cliente_id (str): The ID of the client initiating the transaction.
            contraparte (str | None): The ID of the counterparty involved in the transaction.
            valor (float): The amount of the transaction.
            moeda (MoedaEnum): The currency of the transaction.

        Returns:
            list: A list of alert queries to be executed.
        """
        querys = []

        today = datetime.combine(datetime.now().date(), time.min)
        cliente_transacoes = await cls.get_filtered_transactions(
            cliente_id=cliente_id,
            moeda=moeda,
            tipo=None,
            periodo_inicio=today,
            periodo_fim=None
        )
        triggered_rules = await ComplianceService.get_trigged_rules(
            contraparte=contraparte,
            valor=valor,
            transacoes=cliente_transacoes
        )
        for rule in triggered_rules:
            severidade = SEVERIDADE_ENUM_MAP.get(rule)
            alerta = AlertaRequest(
                cliente_id=cliente_id,
                transacao_id=transacao_id,
                regra=rule,
                severidade=severidade,
                status=StatusEnum.NOVO
            )
            query = await AlertasService.prepare_insert_query(alerta)
            querys.append(query)
        return querys

    @classmethod
    async def get_transaction(cls, transaction_id: str) -> TransacaoResponse:
        """Retrieve a transaction by its ID.

        Args:
            transaction_id (str): The ID of the transaction to retrieve.

        Returns:
            TransacaoResponse: The transaction data.

        Raises:
            TransactionNotFoundException: If no transaction with the given ID exists.
        """
        query = transacoes_table.select().where(transacoes_table.c.id == transaction_id)
        row = await Database.fetch_one(query)
        if not row:
            raise TransactionNotFoundException(transaction_id=transaction_id)
        return TransacaoResponse(**row)

    @classmethod
    async def get_filtered_transactions(
        cls,
        cliente_id: str | None,
        moeda: MoedaEnum | None,
        tipo: TipoTransacaoEnum | None,
        periodo_inicio: datetime | None,
        periodo_fim: datetime | None,
    ) -> list[TransacaoResponse]:
        """Retrieve transactions based on provided filters.

        Args:
            cliente_id (str | None): Filter by client ID.
            moeda (MoedaEnum | None): Filter by currency.
            tipo (TipoTransacaoEnum | None): Filter by transaction type.
            periodo_inicio (datetime | None): Filter by start date.
            periodo_fim (datetime | None): Filter by end date.
        """
        query = transacoes_table.select()

        if cliente_id:
            query = query.where(transacoes_table.c.cliente_id == cliente_id)
        if moeda:
            query = query.where(transacoes_table.c.moeda == moeda.value)
        if tipo:
            query = query.where(transacoes_table.c.tipo == tipo.value)
        if (periodo_inicio and periodo_fim) and periodo_inicio <= periodo_fim:
            query = query.where(
                transacoes_table.c.data_hora.between(periodo_inicio, periodo_fim)
            )
        elif periodo_inicio and not periodo_fim:
            query = query.where(transacoes_table.c.data_hora >= periodo_inicio)
        elif periodo_fim and not periodo_inicio:
            query = query.where(transacoes_table.c.data_hora <= periodo_fim)

        rows = await Database.fetch_all(query)
        return [TransacaoResponse(**row) for row in rows]
