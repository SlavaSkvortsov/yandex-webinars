import asyncio
from dataclasses import dataclass, field
from typing import Any

from httpx import AsyncClient


@dataclass
class MyDataProcessor:
    _client: AsyncClient = field(init=False)

    async def __aenter__(self) -> 'MyDataProcessor':
        self._client = AsyncClient(base_url='https://httpbin.org')
        await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def get_data(self, i: int) -> dict[str, Any]:
        print('Getting data for ', i)
        response = await self._client.get('json')
        print('Got data for ', i)
        return response.json()


async def main() -> None:
    async with MyDataProcessor() as data_processor:
        responses = await asyncio.gather(*(data_processor.get_data(i) for i in range(100)))

    print(responses)


if __name__ == '__main__':
    asyncio.run(main())
