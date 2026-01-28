from watchdog.app.settings import database_settings


class DatabaseConfig:

    db_url = (
        f"postgresql+asyncpg://{database_settings.DB_USER}:{database_settings.DB_PASSWORD}@"
        f"{database_settings.DB_HOST}:{database_settings.DB_PORT}/{database_settings.DB_NAME}"
    )


database_config = DatabaseConfig()
