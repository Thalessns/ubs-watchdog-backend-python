from fastapi import HTTPException, status


class BaseCustomException(HTTPException):

    STATUS_CODE: int = status.HTTP_418_IM_A_TEAPOT
    DETAIL: str = "An error occurred."

    def __init__(self, **kwargs: dict) -> None:
        super().__init__(
            status_code=self.STATUS_CODE, 
            detail=self.DETAIL.format(**kwargs)
        )
