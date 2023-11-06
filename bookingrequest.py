from typing import Optional

from pydantic import BaseModel, Field

from booking import Booking


class BookingRequest(Booking):
    # TODO change to datetime
    created: str

    def __init__(self, id, restaurant, time, created):
        super().__init__(id, restaurant, time)
        self.created = created


# TODO: Name?
class BookingRequestRequest(BaseModel):
    id: Optional[int] = None
    restaurant: str = Field(min_length=2, max_length=100)
    time: str = Field(min_length=8, max_length=20)
    created: str = Field(min_length=8, max_length=20)

    class Config:
        json_schema_extra = {
            'example': {
                'restaurant': 'McDonalds',
                'time': '1970-01-01:19:30:00',
                'created': '1970-01-01:19:30:00'
            }
        }
