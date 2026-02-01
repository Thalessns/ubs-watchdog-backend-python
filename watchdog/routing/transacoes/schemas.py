from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from watchdog.routing.transacoes.enums import TipoTransacaoEnum, MoedaEnum


class TransancaoRequest(BaseModel):

    cliente_id: str
    tipo: TipoTransacaoEnum
    valor: float
    moeda: MoedaEnum
    contraparte: str | None


class TransacaoResponse(BaseModel):

    id: UUID
    cliente_id: UUID
    tipo: TipoTransacaoEnum
    valor: float
    moeda: MoedaEnum
    contraparte: UUID | None
    data_hora: datetime
