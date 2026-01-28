from sqlalchemy.orm import relationship
from sqlalchemy import Column, UUID, String, Enum, DateTime, ForeignKey, DECIMAL

from watchdog.database.database import Base
from watchdog.routing.clientes.enums import RiskLevelEnum, StatusKycEnum
from watchdog.routing.transacoes.enums import TipoTransacaoEnum, MoedaEnum
from watchdog.routing.alertas.enums import SeveridadeEnum, StatusEnum, RegrasEnum


class Clientes(Base):
    __tablename__ = "clientes"

    id = Column(UUID(as_uuid=True), primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    pais = Column(String(50), nullable=False)
    nivel_risco = Column(String(50), nullable=False)
    status_kyc = Column(String(50), nullable=False)
    data_criacao = Column(DateTime, nullable=False)


class Transacoes(Base):
    __tablename__ = "transacoes"

    id = Column(UUID(as_uuid=True), primary_key=True)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    tipo = Column(String(50), nullable=False)
    valor = Column(DECIMAL, nullable=False)
    moeda = Column(String(50), nullable=False)
    contraparte = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=True)
    data_hora = Column(DateTime, nullable=False)

    cliente_rel = relationship("clientes", foreign_keys=[cliente_id])
    contraparte_rel = relationship("clientes", foreign_keys=[contraparte])


class Alertas(Base):
    __tablename__ = "alertas"

    id = Column(UUID(as_uuid=True), primary_key=True)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    transacao_id = Column(UUID(as_uuid=True), ForeignKey("transacoes.id"), nullable=False)
    regra = Column(String(50), nullable=False)
    severidade = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    data_hora = Column(DateTime, nullable=False)

    cliente_rel = relationship("clientes", foreign_keys=[cliente_id])
    transacao_rel = relationship("transacoes", foreign_keys=[transacao_id])


clientes_table = Clientes.__table__
transacoes_table = Transacoes.__table__
alertas_table = Alertas.__table__
