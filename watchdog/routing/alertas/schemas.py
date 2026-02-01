from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from watchdog.routing.alertas.enums import SeveridadeEnum, StatusEnum, RegrasEnum


class AlertaRequest(BaseModel):

    cliente_id: str
    transacao_id: str
    regra: RegrasEnum
    severidade: SeveridadeEnum
    status: StatusEnum


class AlertaResponse(BaseModel):

    id: UUID
    cliente_id: UUID
    transacao_id: UUID
    regra: RegrasEnum
    severidade: SeveridadeEnum
    status: StatusEnum
    data_hora: datetime
