import datetime
from typing import Optional

from pydantic import BaseModel


class Booking:
    id: int
    restaurant: datetime.datetime
    time: datetime.datetime

    def __init__(self, id, restaurant, time):
        self.id = id
        self.restaurant = restaurant
        self.time = time


class BookingRequest(BaseModel):
    id: Optional[int] = None
    restaurant: datetime.datetime
    time: datetime.datetime
