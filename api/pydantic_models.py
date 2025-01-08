from typing import Optional
from pydantic import BaseModel

class CarPriceData(BaseModel):
    car_model: str
    year: int
    price: float
    mileage: int
    color: Optional[str] = None