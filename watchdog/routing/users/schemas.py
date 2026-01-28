from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr

from watchdog.routing.users.enums import RiskLevelEnum, StatusKycEnum


class UserRequest(BaseModel):

    name: str
    email: EmailStr
    pais: str
    nivel_risco: RiskLevelEnum
    status_kyc: StatusKycEnum


class UserResponse(BaseModel):

    id: UUID
    name: str
    email: EmailStr
    pais: str
    nivel_risco: RiskLevelEnum
    status_kyc: StatusKycEnum
    data_criacao: datetime
