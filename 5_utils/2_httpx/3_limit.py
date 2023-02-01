import asyncio
from typing import Any

from httpx import AsyncClient, Limits


async def get_data(client: AsyncClient, i: int) -> dict[str, Any]:
    print('Getting data for ', i)
    response = await client.get('json')
    print('Got data for ', i)
    return response.json()


async def main() -> None:
    client = AsyncClient(
        base_url='https://httpbin.org',
        limits=Limits(max_connections=5, max_keepalive_connections=20),
    )
    async with client:
        responses = await asyncio.gather(*(get_data(client, i) for i in range(100)))

    print(responses)


if __name__ == '__main__':
    asyncio.run(main())
