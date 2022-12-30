from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
import respx
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from my_async_app.db_models import MyTable
from my_async_app.some_functions import (
    NiceClass, fetch_important_data_from_async_function, fetch_important_data_from_database,
    fetch_important_data_from_internet,
)


@pytest.fixture()
def nice_class() -> NiceClass:
    return NiceClass()


@pytest.mark.asyncio()
async def test_fetch_from_db(session: AsyncSession) -> None:
    session.add(MyTable(text_field='some text'))
    session.add(MyTable(text_field='some text2'))
    await session.commit()

    result = await fetch_important_data_from_database()
    assert result == ['some text']


@respx.mock
@pytest.mark.asyncio()
async def test_fetch_from_internet() -> None:
    respx.get('https://httpbin.org/get').respond(json={'some': 'data'})

    response = await fetch_important_data_from_internet()
    assert response == {'some': 'data'}


@patch('my_async_app.some_functions.mock_me')
@pytest.mark.asyncio()
async def test_fetch_from_async_function(mocked_function: AsyncMock) -> None:
    mocked_function.side_effect = Exception('BOOM!')
    result = await fetch_important_data_from_async_function()

    assert result == 1


@pytest.mark.asyncio()
@patch.object(NiceClass, '_mock_me_too', return_value=2007)
# @patch('my_async_app.some_functions.NiceClass._mock_me_too', return_value=1)
async def test_fetch_from_a_nice_class(mocked_function: AsyncMock, nice_class) -> None:
    result = await nice_class.get_nice_number
    result = await nice_class.get_nice_number
    assert result == 2007


@pytest.mark.asyncio()
async def test_fastapi_app(client: AsyncClient) -> None:
    response = await client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.content == b'42'
