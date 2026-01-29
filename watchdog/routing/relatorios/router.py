from datetime import datetime
from fastapi import APIRouter, status

from watchdog.routing.relatorios.schemas import RelatorioResponse
from watchdog.routing.relatorios.service import RelatorioService

relatorio_router = APIRouter(prefix="/relatorios")


@relatorio_router.get("/", status_code=status.HTTP_200_OK, response_model=RelatorioResponse)
async def get_relatorio(
    cliente_id: str,
    periodo_inicio: datetime | None,
    periodo_fim: datetime | None,
) -> RelatorioResponse:
    """Get the report for the given cliente and period.

    Args:
        cliente_id (str): The cliente id.
        periodo_inicio (datetime | None): The start date.
        periodo_fim (datetime | None): The end date.

    Returns:
        RelatorioResponse: The final report.
    """
    return await RelatorioService.get_report(cliente_id, periodo_inicio, periodo_fim)
