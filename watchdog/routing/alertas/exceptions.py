from fastapi import status

from watchdog.app.exceptions import BaseCustomException


class AlertaNotFoundException(BaseCustomException):

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Alerta with the given ID '{id}' was not found."
