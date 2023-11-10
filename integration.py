from typing import Optional

from pydantic import BaseModel, Field


class Integration:
    id: int
    restaurant: str

    def __init__(self, id, restaurant):
        self.id = id
        self.restaurant = restaurant


class IntegrationRequest(BaseModel):
    id: Optional[int] = None
    restaurant: str = Field(min_length=2, max_length=100)
