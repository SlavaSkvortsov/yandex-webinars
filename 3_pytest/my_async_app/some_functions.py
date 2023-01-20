from cached_property import cached_property
from typing import Any

from httpx import AsyncClient
from sqlalchemy import select

from db import Session
from db_models import MyTable
from more_functions import mock_me


async def fetch_important_data_from_database() -> list[str]:
    async with Session() as session:
        query_result = await session.execute(select(MyTable.text_field))

    return query_result.scalars().all()


async def fetch_important_data_from_internet() -> Any:
    async with AsyncClient() as client:
        response = await client.get('https://httpbin.org/get')
        return response.json()


async def fetch_important_data_from_async_function() -> int:
    return await mock_me()


class NiceClass:

    @cached_property
    async def get_nice_number(self) -> int:
        return await self._mock_me_too()

    async def _mock_me_too(self) -> int:
        return 42

    async def _cached_property(self) -> int:
        print('qew')
        return 42
