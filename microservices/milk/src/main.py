from fastapi import FastAPI
import uvicorn
from enum import Enum
from pydantic import BaseModel
from typing import Union
from .db import client
from .dao import Dao


class Milk(BaseModel):
    uid: str
    quantity: int
    price: int = None
    #description: Union[str, None] = None


app = FastAPI()

dao = Dao(client=client)


@app.get("/")
async def root():
    return {"message": "Samskriti Aur Samskar"}

@app.post("/milk/")
async def create(milk: Milk):
    return dao.create(milk.dict())

@app.get("/milk/")
async def get(uid: str):
    return dao.get(uid)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)