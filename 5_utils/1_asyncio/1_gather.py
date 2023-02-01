import asyncio


async def task(n: int) -> int:
    print(f'task {n}')
    await asyncio.sleep(1)
    print(f'task {n} is done')
    return n


async def main() -> None:
    result = await asyncio.gather(*(task(i) for i in range(5)))
    print(sum(result))


if __name__ == '__main__':
    asyncio.run(main())
