from fastapi import status

from watchdog.app.exceptions import BaseCustomException


class ClienteNotFoundException(BaseCustomException):

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Cliente with the specified ID '{id}' was not found."


class ClienteEmailAlreadyExistsException(BaseCustomException):

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Cliente with the specified email '{email}' already exists."
