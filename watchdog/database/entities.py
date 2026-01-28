
from sqlalchemy import Column, UUID, String, Enum, DateTime

from watchdog.database.database import Base
from watchdog.routing.users.enums import RiskLevelEnum, StatusKycEnum


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    pais = Column(String(50), nullable=False)
    nivel_risco = Column(Enum(RiskLevelEnum), nullable=False)
    status_kyc = Column(Enum(StatusKycEnum), nullable=False)
    data_criacao = Column(DateTime, nullable=False)


users_table = Users.__table__
