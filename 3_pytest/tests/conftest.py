import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from _pytest.monkeypatch import MonkeyPatch
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, AsyncTransaction
from my_async_app.config import settings
from my_async_app.db import Base, create_engine, create_sessionmaker
from my_async_app.fastapi_app import app
from tests.db_utils import create_db

settings.database_url = f'{settings.database_url}_test'


@pytest.fixture(scope='session')
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def _create_db() -> None:
    await create_db(url=settings.database_url, base=Base)


@pytest_asyncio.fixture()
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_engine()
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture()
async def db_connection(engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as connection:
        yield connection


@pytest_asyncio.fixture(autouse=True)
async def db_transaction(db_connection: AsyncConnection) -> AsyncGenerator[AsyncTransaction, None]:
    """
    Recipe for using transaction rollback in tests
    https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites  # noqa
    """
    async with db_connection.begin() as transaction:
        yield transaction
        await transaction.rollback()


@pytest_asyncio.fixture(autouse=True)
async def session(db_connection: AsyncConnection, monkeypatch: MonkeyPatch) -> AsyncGenerator[AsyncSession, None]:
    session_maker = create_sessionmaker(db_connection)
    monkeypatch.setattr('my_async_app.some_functions.Session', session_maker)

    async with session_maker() as session:
        yield session


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
