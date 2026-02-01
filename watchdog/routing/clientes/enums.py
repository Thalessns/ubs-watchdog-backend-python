from enum import Enum


class RiskLevelEnum(Enum):

    BAIXO = "Baixo"
    MEDIO = "Medio"
    ALTO = "Alto"


class StatusKycEnum(Enum):

    PENDENTE = "Pendente"
    APROVADO = "Aprovado"
    REJEITADO = "Rejeitado"
