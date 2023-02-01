import asyncio
from functools import partial
from operator import eq

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1), retry_on_exeption=retry_if_result(partial(eq, 1)))
async def task(n: int) -> int:
    print(f'task {n}')
    await asyncio.sleep(1)
    print(f'task {n} is done')
    return n


async def main() -> None:
    result = await asyncio.gather(*(task(i) for i in range(5)))
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
