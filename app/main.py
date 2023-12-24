import demo
from fastapi import FastAPI, BackgroundTasks

from schemas import Car
from database import DB, Filter, Sort
from typing import Literal, List


app = FastAPI()


@app.on_event("startup")
async def on_start(): 
    demo.import_cars()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/import")
def import_cars(background_tasks: BackgroundTasks) -> None:
    background_tasks.add_task(demo.import_cars)


@app.get("/cars", response_model=list[Car])
def get_all(
    brand: str | None  = None,
    typename: str | None  = None,
    year_min: int | None  = None,
    year_max: int | None  = None,
    mileage_min: int | None  = None,
    mileage_max: int | None  = None,
    dealer: str | None  = None,
    rating_min: int | None  = None,
    rating_max: int | None  = None,
    reviews_min: int | None  = None,
    reviews_max: int | None  = None,
    price_min: int | None  = None,
    price_max: int | None = None,
    sortBy: str | None = None,
    orderAsc: bool = True
) -> list[Car]:
    filters: List[Filter] = [
        ("brand", brand),
        ("typename", typename),
        ("year", year_min, year_max),
        ("mileage", mileage_min, mileage_max),
        ("dealer", dealer),
        ("rating", rating_min, rating_max),
        ("reviews", reviews_min, reviews_max),
        ("price", price_min, price_max),
    ]

    order: Literal["ASC", "DESC"] = "ASC" if orderAsc else "DESC"
    sort: Sort | None = (sortBy, order) if sortBy else None

    return DB.all(sort, filters)
