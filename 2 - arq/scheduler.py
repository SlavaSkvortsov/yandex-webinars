from dataclasses import dataclass, field
from typing import Generator


@dataclass
class Scheduler:
    running_jobs: list[Generator] = field(default_factory=list)

    def add_job(self, job: 'Job') -> None:
        self.running_jobs.append(job.run())

    def run(self):
        while True:
            try:
                for job in self.running_jobs:
                    next(job)


            except StopIteration:
                print('Job finished')
                break


@dataclass
class Job:
    name: str

    def run(self):
        for i in range(10):
            print(self.name, i)
            _ = (yield)


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.add_job(Job('Job 1'))
    scheduler.add_job(Job('Job 2'))
    scheduler.run()