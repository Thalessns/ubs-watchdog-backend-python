from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr

from watchdog.routing.clientes.enums import RiskLevelEnum, StatusKycEnum
from watchdog.routing.transacoes.enums import MoedaEnum, TipoTransacaoEnum
from watchdog.routing.alertas.enums import RegrasEnum, SeveridadeEnum, StatusEnum


class TransacaoRelatorio(BaseModel):

    id: UUID
    tipo: TipoTransacaoEnum
    moeda: MoedaEnum
    valor: float
    contraparte: UUID | None
    data_hora: datetime


class TransacoesInfo(BaseModel):

    numero_transacoes: int
    transacoes: list[TransacaoRelatorio]
    valor_usd: float
    valor_eur: float
    valor_brl: float


class AlertaRelatorio(BaseModel):
    
    id: UUID
    transacao_id: UUID
    regra: RegrasEnum
    severidade: SeveridadeEnum
    status: StatusEnum
    data_hora: datetime


class AlertasInfo(BaseModel):
    
    numero_alertas: int
    alertas: list[AlertaRelatorio]
    limite_diario: int
    fracionamento: int
    paises_suspeitos: int


class RelatorioResponse(BaseModel):

    cliente_id: UUID
    nome: str
    email: EmailStr
    pais: str
    nivel_risco: RiskLevelEnum
    status_kyc: StatusKycEnum
    transacoes_info: TransacoesInfo
    alertas_info: AlertasInfo
