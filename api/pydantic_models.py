from typing import Optional
from pydantic import BaseModel

class CarPriceData(BaseModel):
    id: int = 149990878
    list_id: int = 109913621
    list_time: int = 1694606265000
    manufacture_date: int = 2011
    brand: str = 'Ford'
    model: str = 'Fiesta'
    origin: str = 'Thái Lan'
    type: str = 'Hatchback'
    seats: float = 5.0
    gearbox: str = 'AT'
    fuel: str = 'petrol'
    color: str = 'white'
    mileage_v2: int = 10000
    condition: str = 'used'