from typing import Any

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class MyAmazingModel(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='John Cena')


class MyAmazingResponseModel(BaseModel):
    id: int = Field(example=2)
    name: str = Field(example='John Cena')
    age: int = Field(example=30)


@app.post('/foo', response_model=MyAmazingResponseModel)
async def foo(data: MyAmazingModel) -> Any:
    pass


if __name__ == '__main__':
    uvicorn.run(app)
