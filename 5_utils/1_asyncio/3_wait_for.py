import asyncio


async def task(n: int) -> int:
    print(f'task {n}')
    await asyncio.sleep(1)
    print(f'task {n} is done')
    return n


async def main() -> None:
    result = await asyncio.wait_for(task(1), timeout=2)
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
