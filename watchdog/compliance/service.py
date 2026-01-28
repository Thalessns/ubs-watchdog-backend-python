from watchdog.routing.clientes.service import ClientesService
from watchdog.routing.transacoes.schemas import TransacaoResponse
from watchdog.routing.alertas.enums import RegrasEnum, PaisesSuspeitosEnum
from watchdog.compliance.config import values_limit


class ComplianceService:

    @classmethod
    async def get_trigged_rules(
        cls, 
        contraparte: str | None,
        valor: float,
        transacoes: list[TransacaoResponse]
    ) -> list[RegrasEnum]:
        """Verify if a transaction triggers any compliance rules.

        Args:
            contraparte (str | None): The ID of the counterparty involved in the transaction.
            valor (float): The amount of the transaction.
            transacoes (list[TransacaoResponse]): List of previous transactions for the client.

        Returns:
            list[RegrasEnum] | None: A list of triggered rules or None if no rules are triggered.
        """
        triggered_rules = []

        if await cls.verify_max_transaction_amount(valor, transacoes):
            triggered_rules.append(RegrasEnum.LIMITE_DIARIO)
        if await cls.verify_frequent_transactions(transacoes):
            triggered_rules.append(RegrasEnum.TRANSACOES_REPETIDAS)
        if await cls.verify_paises_de_risco(contraparte):
            triggered_rules.append(RegrasEnum.PAISES_SUSPEITOS)

        return triggered_rules

    @classmethod
    async def verify_max_transaction_amount(
        cls,
        valor: float,
        transacoes: list[TransacaoResponse]
    ) -> bool:
        """Check if the client has exceeded the maximum transaction amount.

        Args:
            valor (float): The amount of the transaction.
            transacoes (list[TransacaoResponse]): List of previous transactions for the client.

        Returns:
            bool: True if the maximum amount is exceeded, False otherwise.
        """
        valor_total = 0
        for transacao in transacoes:
            valor_total += transacao.valor

        if valor_total + valor > values_limit.LIMIT_AMMOUNT:
            return True
        return False

    @classmethod
    async def verify_frequent_transactions(
        cls,
        transacoes: list[TransacaoResponse]
    ) -> bool:
        """Check if the client has made frequent transactions.

        Args:
            transacoes (list[TransacaoResponse]): List of previous transactions for the client.

        Returns:
            bool: True if frequent transactions are detected, False otherwise.
        """
        count = 0
        for transacao in transacoes:
            if transacao.valor < values_limit.MAX_LOW_AMMOUNT:
                count += 1
        if count < values_limit.MAX_LOW_AMMOUNT_TIMES:
            return False
        return True

    @classmethod
    async def verify_paises_de_risco(cls, contraparte: str | None) -> bool:
        """Check if a country is considered high-risk.

        Args:
            contraparte (str | None): The ID of the counterparty involved in the transaction.

        Returns:
            bool: True if the country is high-risk, False otherwise.
        """
        if contraparte:
            contrapar = await ClientesService.get_cliente_by_id(contraparte)
            for pais in PaisesSuspeitosEnum:
                if contrapar.pais == pais.value:
                    return True
        return False
