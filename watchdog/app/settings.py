from pydantic_settings import BaseSettings


class EntryPointSettings(BaseSettings):

    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 6000
    APP_RELOAD: bool = False


class DatabaseSettings(BaseSettings):

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int


entry_settings = EntryPointSettings()
database_settings = DatabaseSettings()
