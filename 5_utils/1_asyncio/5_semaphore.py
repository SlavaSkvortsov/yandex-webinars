import asyncio
from dataclasses import dataclass, field


@dataclass
class SomeClient:
    _some_key: str | None = None
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    _semaphore: asyncio.Semaphore = field(default_factory=lambda: asyncio.Semaphore(2))

    async def get_some_data(self, item_id: int) -> str:
        self._some_key = await self._get_some_key()
        return await self._get_some_data(item_id)

    async def _get_some_key(self) -> str:
        async with self._lock:
            if self._some_key is None:
                print('Log in to get the key')
                await asyncio.sleep(1)
                self._some_key = 'secret_key'
        return self._some_key

    async def _get_some_data(self, item_id: int) -> str:
        async with self._semaphore:
            print('Getting some data')
            await asyncio.sleep(1)
        return f'{self._some_key} {item_id}'


async def main() -> None:
    client = SomeClient()
    result = await asyncio.gather(*(client.get_some_data(i) for i in range(5)))
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
