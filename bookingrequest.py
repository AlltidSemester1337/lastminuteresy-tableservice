import datetime
import json

from pydantic import BaseModel, Field


class BookingRequest:
    integration_id: int
    restaurant: str
    time: datetime.datetime
    created: datetime.datetime

    def __init__(self, integration_id, restaurant, time, created):
        self.integration_id = integration_id
        self.restaurant = restaurant
        self.time = time
        self.created = created

    class BookingRequestEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, BookingRequest):
                return {"integration_id": obj.integration_id, "restaurant": obj.restaurant, "time": str(obj.time), "created": str(obj.created)}
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
