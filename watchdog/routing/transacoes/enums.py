from enum import Enum


class TipoTransacaoEnum(Enum):

    DEPOSITO = "Deposito"
    SAQUE = "Saque"
    TRANSFERENCIA = "Transferencia"


class MoedaEnum(Enum):
    
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"
