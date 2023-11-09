import datetime
import json

from pydantic import BaseModel, Field


class BookingRequest:
    restaurant: datetime.datetime
    time: datetime.datetime
    created: datetime.datetime

    def __init__(self, restaurant, time, created):
        self.restaurant = restaurant
        self.time = time
        self.created = created

    class BookingRequestEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, BookingRequest):
                return {"restaurant": obj.restaurant, "time": str(obj.time), "created": str(obj.created)}
            return super().default(obj)


# TODO: Name?
class BookingRequestRequest(BaseModel):
    restaurant: str = Field(min_length=2, max_length=100)
    time: datetime.datetime

    class Config:
        json_schema_extra = {
            'example': {
                'restaurant': 'McDonalds',
                'time': '2023-11-09T12:30:00'
            }
        }
