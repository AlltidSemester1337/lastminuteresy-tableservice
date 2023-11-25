import datetime
import json

from pydantic import BaseModel, Field


class BookingRequest:
    integration_id: int
    restaurant: str
    time: datetime.datetime
    num_persons: int
    extra_parameters: dict
    created: datetime.datetime

    def __init__(self, integration_id, restaurant, num_persons, extra_parameters, time, created):
        self.integration_id = integration_id
        self.restaurant = restaurant
        self.num_persons = num_persons
        self.extra_parameters = extra_parameters
        self.time = time
        self.created = created

    class BookingRequestEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, BookingRequest):
                return {"integration_id": obj.integration_id, "restaurant": obj.restaurant,
                        "num_persons": obj.num_persons, "extra_parameters": obj.extra_parameters, "time": str(obj.time),
                        "created": str(obj.created)}
            return super().default(obj)


# TODO: Name?
class BookingRequestRequest(BaseModel):
    integration_id: int = Field(gt=0, alias="integrationId")
    time: datetime.datetime
    num_persons: int = Field(gt=1, alias="numPersons")
    extra_parameters: dict = Field(alias="extraParameters")

    class Config:
        json_schema_extra = {
            'example': {
                'integrationId': 1,
                'time': '2023-11-09T12:30:00',
                'numPersons': 2,
                'extraParameters': {'email': 'test@test.com'}
            }
        }
