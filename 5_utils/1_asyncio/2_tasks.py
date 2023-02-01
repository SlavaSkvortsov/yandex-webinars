import asyncio


async def task(n: int) -> int:
    print(f'task {n}')
    await asyncio.sleep(1)
    print(f'task {n} is done')
    return n


async def main() -> None:
    one = asyncio.create_task(task(1))
    two = asyncio.create_task(task(2))

    print('Some other stuff')
    await asyncio.sleep(2)
    print('Some other stuff is done')

    await one
    await two


if __name__ == '__main__':
    asyncio.run(main())
