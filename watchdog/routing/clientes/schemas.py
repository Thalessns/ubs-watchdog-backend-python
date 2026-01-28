from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr

from watchdog.routing.clientes.enums import RiskLevelEnum, StatusKycEnum


class ClienteRequest(BaseModel):

    nome: str
    email: EmailStr
    pais: str
    nivel_risco: RiskLevelEnum
    status_kyc: StatusKycEnum


class ClienteResponse(BaseModel):

    id: UUID
    nome: str
    email: EmailStr
    pais: str
    nivel_risco: RiskLevelEnum
    status_kyc: StatusKycEnum
    data_criacao: datetime
