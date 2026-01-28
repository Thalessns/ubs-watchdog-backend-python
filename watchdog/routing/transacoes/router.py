from datetime import datetime
from fastapi import APIRouter, status

from watchdog.routing.transacoes.enums import TipoTransacaoEnum, MoedaEnum
from watchdog.routing.transacoes.schemas import (
    TransancaoRequest,
    TransacaoResponse
)
from watchdog.routing.transacoes.service import TransacoesService


transacoes_router = APIRouter(prefix="/transacoes")


@transacoes_router.post("/", status_code=status.HTTP_201_CREATED, response_model=TransacaoResponse)
async def create(transacao: TransancaoRequest) -> TransacaoResponse:
    """Create a new transaction.

    Args:
        transacao (TransancaoRequest): Transaction data.

    Returns:
        TransacaoResponse: Created transaction details.
    """
    return await TransacoesService.create(transacao)


@transacoes_router.get("/by-id", status_code=status.HTTP_200_OK, response_model=TransacaoResponse)
async def get_by_id(id: str) -> TransacaoResponse:
    """Retrieve a transaction by its ID.

    Args:
        id (str): Transaction ID.

    Returns:
        TransacaoResponse: Transaction details.
    """
    return await TransacoesService.get_transaction(id)


@transacoes_router.get("/filter", status_code=status.HTTP_200_OK, response_model=list[TransacaoResponse])
async def get_by_filter(
    cliente_id: str | None = None,
    moeda: MoedaEnum | None = None,
    tipo: TipoTransacaoEnum | None = None,
    periodo_inicio: datetime | None = None,
    periodo_fim: datetime | None = None,
) -> list[TransacaoResponse]:
    """Retrieve transactions based on filters.

    Args:
        cliente_id (str | None, optional): Client ID filter. Defaults to None.
        moeda (MoedaEnum | None, optional): Currency filter. Defaults to None.
        tipo (TipoTransacaoEnum | None, optional): Transaction type filter. Defaults to None
        periodo_inicio (datetime | None, optional): Start date filter. Defaults to None.
        periodo_fim (datetime | None, optional): End date filter. Defaults to None.

    Returns:
        list[TransacaoResponse]: List of transactions matching the filters.
    """
    return await TransacoesService.get_filtered_transactions(
        cliente_id=cliente_id,
        moeda=moeda,
        tipo=tipo,
        periodo_inicio=periodo_inicio,
        periodo_fim=periodo_fim
    )
