from constants import MY_QUEUE
from job import my_async_job


class WorkerSettings:
    functions = [my_async_job]
    queue_name = MY_QUEUE

