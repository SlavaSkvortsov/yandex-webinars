import asyncio
from urllib.parse import urljoin

import arq
from typing import Any

import httpx

from constants import MY_QUEUE


async def my_async_job(ctx: dict[str, Any], delay: int) -> None:
    await asyncio.sleep(delay * 100)


async def main() -> None:
    redis = await arq.create_pool()
    await redis.enqueue_job('my_async_job', 2, _queue_name=MY_QUEUE)
    await redis.close()

if __name__ == '__main__':
    asyncio.run(main())
