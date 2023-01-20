from fastapi import FastAPI

from more_functions import mock_me

app = FastAPI()


@app.get("/")
async def root() -> int:
    return await mock_me()
