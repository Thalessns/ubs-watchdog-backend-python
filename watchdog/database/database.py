from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine

from watchdog.database.config import database_config

Base = declarative_base(metadata=MetaData())
engine = create_async_engine(database_config.db_url)


class Database:

    @staticmethod
    async def fetch_one(query) -> dict | None:
        async with engine.connect() as conn:
            cursor = await conn.execute(query)
            row = cursor.fetchone()
            return (row._mapping) if row else None

    @staticmethod
    async def fetch_all(query) -> list[dict] | None:
        async with engine.connect() as conn:
            cursor = await conn.execute(query)
            rows = cursor.fetchall()
            return [(row._mapping) for row in rows]

    @staticmethod
    async def execute(query) -> None:
        async with engine.begin() as conn:
            await conn.execute(query)

    @staticmethod
    async def execute_many(queries: list) -> None:
        async with engine.begin() as conn:
            for query in queries:
                await conn.execute(query)

    @staticmethod
    async def init_models() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
