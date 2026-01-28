from fastapi import status

from watchdog.app.exceptions import BaseCustomException


class DatabaseOperationException(BaseCustomException):
    
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "An error occurred while performing a database operation. {error}"
