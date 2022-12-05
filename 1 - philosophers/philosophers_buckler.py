import threading
import time
from dataclasses import dataclass, field
from enum import Enum


PHILOSOPHERS = 5
TIMEOUT = 5
WAIT = 0.5


@dataclass
class Fork:
    lock: threading.Lock = field(default_factory=threading.Lock)

    def acquire(self, blocking: bool = True) -> bool:
        return self.lock.acquire(blocking=blocking)

    def release(self) -> None:
        if self.lock.locked():
            self.lock.release()


class Side(str, Enum):
    LEFT = 'left'
    RIGHT = 'right'


@dataclass
class Philosopher:
    fork: dict[Side, Fork]
    name: str
    buckler: threading.Semaphore
    ate_count: int = 0

    def run(self) -> None:
        begin = time.monotonic()
        while time.monotonic() - begin < TIMEOUT:
            with self.buckler:
                self._eat()
            self._think()

    def _eat(self) -> None:
        self._acquire_fork(Side.LEFT)
        self._acquire_fork(Side.RIGHT)

        print(f'{self.name} is eating')
        time.sleep(WAIT)
        self.ate_count += 1
        self._release_fork(Side.LEFT)
        self._release_fork(Side.RIGHT)

    def _acquire_fork(self, side: Side) -> bool:
        print(f'{self.name} is trying to acquire {side} fork')
        fork = self.fork[side]
        time.sleep(WAIT)
        return fork.acquire()

    def _release_fork(self, side: Side) -> None:
        fork = self.fork[side]
        fork.release()

    def _think(self) -> None:
        print(f'{self.name} is thinking')
        time.sleep(WAIT)


def main() -> None:
    buckler = threading.Semaphore(PHILOSOPHERS - 1)
    forks = [Fork() for _ in range(PHILOSOPHERS)]
    philosophers = [
        Philosopher(
            name=f'Philosopher {i}',
            buckler=buckler,
            fork={
                Side.LEFT: forks[i],
                Side.RIGHT: forks[(i + 1) % 5],
            },
        ) for i in range(5)
    ]

    threads = [threading.Thread(target=philosopher.run) for philosopher in philosophers]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.stop = True
        thread.join()

    print('Philosophers ate:')
    for philosopher in philosophers:
        print(f'{philosopher.name}: {philosopher.ate_count}')


if __name__ == '__main__':
    main()
