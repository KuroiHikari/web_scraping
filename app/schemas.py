from pydantic import BaseModel
from decimal import Decimal

class Car(BaseModel):
    id: int
    name: str
    mileage: Decimal
    dealer: str
    rating: Decimal
    reviews: int
    price: int
