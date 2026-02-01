from pydantic_settings import BaseSettings


class ValuesLimitConfig(BaseSettings):

    LIMIT_AMMOUNT: float = 1000
    MAX_LOW_AMMOUNT: float = 50
    MAX_LOW_AMMOUNT_TIMES: int = 6


values_limit = ValuesLimitConfig()
