from enum import Enum


class RegrasEnum(Enum):

    LIMITE_DIARIO = "Limite Diario"
    PAISES_SUSPEITOS = "Paises Suspeitos"
    TRANSACOES_REPETIDAS = "Transacoes Repetidas"


class SeveridadeEnum(Enum):

    BAIXA = "Baixa"
    MEDIA = "Media"
    ALTA = "Alta"


class StatusEnum(Enum):

    NOVO = "Novo"
    EM_ANALISE = "Em Analise"
    RESOLVIDO = "Resolvido"


class PaisesSuspeitosEnum(Enum):

    COREIA_NORTE = "Coreia do Norte"
    IRAN = "Iran"
    SIRIA = "Siria"
    CUBA = "Cuba"


SEVERIDADE_ENUM_MAP = {
    RegrasEnum.LIMITE_DIARIO: SeveridadeEnum.BAIXA,
    RegrasEnum.TRANSACOES_REPETIDAS: SeveridadeEnum.MEDIA,
    RegrasEnum.PAISES_SUSPEITOS: SeveridadeEnum.ALTA,
}
