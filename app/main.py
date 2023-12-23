from fastapi import FastAPI

from schemas import Car
from database import DB

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/cars", response_model=list[Car])
def get_all(
    brand = None,
    typeName = None,
    year_min = None,
    year_max = None,
    mileage_min = None,
    mileage_max = None,
    dealer = None,
    rating_min = None,
    rating_max = None,
    reviews_min = None,
    reviews_max = None,
    price_min = None,
    price_max = None,
    sortBy = None
) -> list[Car]:
    filters = [
        ("brand", brand),
        ("typeName", typeName),
        ("year", year_min, year_max),
        ("mileage", mileage_min, mileage_max),
        ("dealer", dealer),
        ("rating", rating_min, rating_max),
        ("reviews", reviews_min, reviews_max),
        ("price", price_min, price_max),
    ]


    return DB.all(sortBy, filters)
