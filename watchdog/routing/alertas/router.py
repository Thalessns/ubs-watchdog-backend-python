from datetime import datetime
from fastapi import APIRouter, status

from watchdog.routing.alertas.enums import RegrasEnum, SeveridadeEnum, StatusEnum
from watchdog.routing.alertas.schemas import AlertaResponse
from watchdog.routing.alertas.service import AlertasService

alertas_router = APIRouter(prefix="/alertas")


@alertas_router.get("/by-id", status_code=status.HTTP_200_OK, response_model=AlertaResponse)
async def get_alerta_by_id(id: str) -> AlertaResponse:
    """Get alerta by ID endpoint.

    Args:
        id (str): The ID of the alerta to retrieve.

    Returns:
        AlertaResponse: The alerta data.
    """
    return await AlertasService.get_alerta_by_id(id)


@alertas_router.get("/by-transacao-id", status_code=status.HTTP_200_OK, response_model=list[AlertaResponse])
async def get_alertas_by_transacao_id(transacao_id: str) -> list[AlertaResponse]:
    """Get alertas by transaction ID endpoint.

    Args:
        transacao_id (str): The ID of the transaction to retrieve alertas for.

    Returns:
        list[AlertaResponse]: A list of alertas associated with the transaction.
    """
    return await AlertasService.get_alertas_by_transacao_id(transacao_id)


@alertas_router.get("/filter", status_code=status.HTTP_200_OK, response_model=list[AlertaResponse])
async def get_filtered_alertas(
    cliente_id: str | None = None,
    regra: RegrasEnum | None = None,
    severidade: SeveridadeEnum | None = None,
    status: StatusEnum | None = None,
    periodo_inicio: datetime | None = None,
    periodo_fim: datetime | None = None,
) -> list[AlertaResponse]:
    """Get filtered alertas endpoint.

    Args:
        cliente_id (str | None): Filter by client ID.
        regra (RegrasEnum | None): Filter by rule.
        severidade (SeveridadeEnum | None): Filter by severity.
        status (StatusEnum | None): Filter by status.
        periodo_inicio (datetime | None): Filter by start of the period.
        periodo_fim (datetime | None): Filter by end of the period.

    Returns:
        list[AlertaResponse]: A list of filtered alertas.
    """
    return await AlertasService.get_filtered_alertas(
        cliente_id=cliente_id,
        regra=regra,
        severidade=severidade,
        status=status,
        periodo_inicio=periodo_inicio,
        periodo_fim=periodo_fim,
    )
