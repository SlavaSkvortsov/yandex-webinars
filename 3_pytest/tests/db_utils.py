from dataclasses import dataclass
from functools import cached_property

from sqlalchemy import text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine, create_async_engine,
)
from sqlalchemy.orm import DeclarativeMeta


@dataclass
class DBUtils:
    url: str

    @cached_property
    def postgres_engine(self) -> AsyncEngine:
        url_params = self._parsed_url._asdict()
        url_params['database'] = 'postgres'
        url_with_postgres_db = URL.create(**url_params)
        return create_async_engine(url_with_postgres_db, isolation_level='AUTOCOMMIT')

    @cached_property
    def db_engine(self) -> AsyncEngine:
        return create_async_engine(self.url, isolation_level='AUTOCOMMIT')

    async def create_database(self) -> None:
        query = text(f"CREATE DATABASE {self._parsed_url.database} ENCODING 'utf8'")
        async with self.postgres_engine.connect() as conn:
            await conn.execute(query)

    async def create_tables(self, base: DeclarativeMeta) -> None:
        async with self.db_engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)

    async def drop_database(self) -> None:
        query = text(f'DROP DATABASE {self._parsed_url.database}')
        async with self.postgres_engine.begin() as conn:
            await conn.execute(query)

    async def database_exists(self) -> bool:
        query = text('SELECT 1 FROM pg_database WHERE datname = :database')
        async with self.postgres_engine.connect() as conn:
            query_result = await conn.execute(query, {'database': self._parsed_url.database})
        result = query_result.scalar()
        return bool(result)

    @cached_property
    def _parsed_url(self) -> URL:
        return make_url(self.url)


async def create_db(url: str, base: DeclarativeMeta) -> None:
    db_utils = DBUtils(url=url)

    try:
        if await db_utils.database_exists():
            await db_utils.drop_database()

        await db_utils.create_database()
        await db_utils.create_tables(base)
    finally:
        await db_utils.postgres_engine.dispose()
        await db_utils.db_engine.dispose()
