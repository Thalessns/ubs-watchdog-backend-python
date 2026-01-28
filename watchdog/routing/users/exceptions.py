from fastapi import status

from watchdog.app.exceptions import BaseCustomException


class UserNotFoundException(BaseCustomException):

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "User with the specified ID '{id}' was not found."


class UserEmailAlreadyExistsException(BaseCustomException):

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "User with the specified email '{email}' already exists."
