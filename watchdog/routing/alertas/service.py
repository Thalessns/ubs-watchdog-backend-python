from uuid import uuid4
from datetime import datetime

from watchdog.database.database import Database
from watchdog.database.entities import alertas_table
from watchdog.routing.alertas.enums import RegrasEnum, SeveridadeEnum, StatusEnum
from watchdog.routing.alertas.exceptions import AlertaNotFoundException
from watchdog.routing.alertas.schemas import AlertaRequest, AlertaResponse


class AlertasService:

    @classmethod
    async def prepare_insert_query(cls, alerta: AlertaRequest):
        """Prepare the insert query for a new alerta.
        
        Args:
            alerta (AlertaRequest): The alerta data to insert.

        Returns:
        """
        new_id = uuid4()
        date_created = datetime.now()

        return alertas_table.insert().values(
            id = new_id,
            cliente_id = alerta.cliente_id,
            transacao_id = alerta.transacao_id,
            regra = alerta.regra.value,
            severidade = alerta.severidade.value,
            status = alerta.status.value,
            data_hora = date_created
        )

    @classmethod
    async def get_alerta_by_id(cls, alerta_id: str) -> AlertaResponse:
        """Get alerta by ID from the database.

        Args:
            alerta_id (str): The ID of the alerta to retrieve.            

        Returns:
            AlertaResponse: The alerta data.

        Raises:
            AlertaNotFoundException: If no alerta is found with the given ID.
        """
        query = alertas_table.select().where(alertas_table.c.id == alerta_id)
        row = await Database.fetch_one(query)
        if not row:
            raise AlertaNotFoundException(id=alerta_id)
        return AlertaResponse(**row)

    @classmethod
    async def get_alertas_by_transacao_id(cls, transacao_id: str) -> list[AlertaResponse]:
        """Get alertas by transaction ID from the database.

        Args:
            transacao_id (str): The ID of the transaction to retrieve alertas for.

        Returns:
            list[AlertaResponse]: A list of alertas associated with the transaction.
        """
        query = alertas_table.select().where(alertas_table.c.transacao_id == transacao_id)
        rows = await Database.fetch_all(query)
        return [AlertaResponse(**row) for row in rows] if rows else []

    @classmethod
    async def get_filtered_alertas(
        cls,
        cliente_id: str | None,
        regra: RegrasEnum | None,
        severidade: SeveridadeEnum | None,
        status: StatusEnum | None,
        periodo_inicio: datetime | None,
        periodo_fim: datetime | None,
    ) -> list[AlertaResponse]:
        """Get alertas filtered by various criteria.
        
        Args:
            cliente_id (str | None): Filter by client ID.
            regra (RegrasEnum | None): Filter by rule.
            severidade (SeveridadeEnum | None): Filter by severity.
            status (StatusEnum | None): Filter by status.
            periodo_inicio (datetime | None): Filter by start of date range.
            periodo_fim (datetime | None): Filter by end of date range.
        """
        query = alertas_table.select()

        if cliente_id:
            query = query.where(alertas_table.c.cliente_id == cliente_id)
        if regra:
            query = query.where(alertas_table.c.regra == regra.value)
        if severidade:
            query = query.where(alertas_table.c.severidade == severidade.value)
        if status:
            query = query.where(alertas_table.c.status == status.value)
        if (periodo_inicio and periodo_fim) and (periodo_inicio <= periodo_fim):
            query = query.where(
                alertas_table.c.data_hora.between(periodo_inicio, periodo_fim)
            )
        elif periodo_inicio:
            query = query.where(alertas_table.c.data_hora >= periodo_inicio)
        elif periodo_fim:
            query = query.where(alertas_table.c.data_hora <= periodo_fim)
        
        rows = await Database.fetch_all(query)
        return [AlertaResponse(**row) for row in rows] if rows else []
