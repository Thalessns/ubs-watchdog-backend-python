from fastapi import status

from watchdog.app.exceptions import BaseCustomException


class TransactionNotFoundException(BaseCustomException):
    
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Transaction with ID '{transaction_id}' not found."
