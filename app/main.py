from fastapi import FastAPI

from schemas import Car
from database import DB

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/cars", response_model=list[Car])
def get_all() -> list[Car]:
    return DB.all()
