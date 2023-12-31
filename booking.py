import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Booking:
    id: int
    restaurant: str
    time: datetime.datetime

    def __init__(self, id, restaurant, time):
        self.id = id
        self.restaurant = restaurant
        self.time = time


class BookingRequest(BaseModel):
    id: Optional[int] = None
    restaurant: str = Field(min_length=2, max_length=100)
    time: datetime.datetime
