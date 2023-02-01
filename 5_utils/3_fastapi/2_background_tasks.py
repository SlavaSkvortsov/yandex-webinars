import asyncio
from typing import Any

import uvicorn
from fastapi import BackgroundTasks, FastAPI
from starlette import status

app = FastAPI()


async def add_to_file(text: str) -> None:
    await asyncio.sleep(5)
    with open('file.txt', 'a') as f:
        f.write(text)
        f.write('\n')


@app.post('/foo', status_code=status.HTTP_202_ACCEPTED)
async def foo(text: str, background_tasks: BackgroundTasks) -> Any:
    background_tasks.add_task(add_to_file, text)


if __name__ == '__main__':
    uvicorn.run(app)
