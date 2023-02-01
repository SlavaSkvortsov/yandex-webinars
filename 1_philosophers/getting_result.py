import time
from concurrent.futures import ProcessPoolExecutor


def task() -> str:
    print('Task started')
    time.sleep(1)
    print('Task finished')
    return f'done {1}'


def main() -> None:
    with ProcessPoolExecutor() as executor:
        # result = executor.map(task, range(5))
        #
        # for item in result:
        #     print(item)
        futures = [executor.submit(task) for _ in range(5)]
        results = [future.result() for future in futures]
        print(results)


if __name__ == '__main__':
    main()
