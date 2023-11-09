import datetime
from typing import Optional

from pydantic import BaseModel, Field

from booking import Booking


class BookingRequest(Booking):
    # TODO change to datetime
    created: datetime.datetime

    def __init__(self, id, restaurant, time, created):
        super().__init__(id, restaurant, time)
        self.created = created


# TODO: Name?
class BookingRequestRequest(BaseModel):
    id: Optional[int] = None
    restaurant: str = Field(min_length=2, max_length=100)
    time: datetime.datetime

    class Config:
        json_schema_extra = {
            'example': {
                'restaurant': 'McDonalds',
                'time': '2023-11-09T12:30:00'
            }
        }
