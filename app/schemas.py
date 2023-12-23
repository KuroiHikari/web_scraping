from pydantic import BaseModel
from decimal import Decimal

class Car(BaseModel):
    id: int
    brand: str
    typeName: str
    year: int
    mileage: Decimal
    dealer: str
    rating: Decimal
    reviews: int
    price: int
