import asyncio
from typing import Any
from urllib.parse import urljoin

from httpx import AsyncClient


async def get_data(client: AsyncClient) -> dict[str, Any]:
    response = await client.get('json')
    return response.json()


async def main() -> None:
    client = AsyncClient(base_url='https://httpbin.org/some-api/v3')
    async with client:
        responses = await asyncio.gather(*(get_data(client) for _ in range(5)))

    print(responses)


if __name__ == '__main__':
    print(urljoin('https://httpbin.org/some-api/v3', '/json'))
    # asyncio.run(main())
