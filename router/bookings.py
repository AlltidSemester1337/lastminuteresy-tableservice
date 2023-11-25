import datetime
from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from sqlalchemy.orm import Session

import main
from bookingrequest import BookingRequest, BookingRequestRequest
from database import SessionLocal
import models
from google.cloud import pubsub_v1
import json

from router import integrations, dependencies

project_id = "sapient-bucksaw-401016"
topic_id = "booking-requests"
# TODO this secret needs to be added manually... should be improved
SERVICE_ACCOUNT_PATH = './sapient-bucksaw-401016-4a1b2964cb2f.json'
# For local run with default SA (granted it has pub/sub permissions) use below
# publisher = pubsub_v1.PublisherClient()
publisher = pubsub_v1.PublisherClient.from_service_account_json(SERVICE_ACCOUNT_PATH)
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
)

db_dep = Annotated[Session, Depends(dependencies.get_db)]


@router.get("/free/all")
def get_all_free_bookings(db: db_dep):
    return db.query(models.Bookings).all()


@router.get("/free")
def get_all_free_bookings_by_name(db: db_dep, restaurant_name: str = Query(min_length=2, max_length=100)):
    return db.query(models.Bookings).all().filter(models.Bookings.restaurant.casefold() == restaurant_name.casefold())


@router.delete("/{id}", status_code=204)
def delete_booking(id: int = Path(gt=-1), db=db_dep):
    db.query(models.Bookings).filter(models.Bookings.id == id).delete()


# TODO In a future version we should support the caller to select the integration
@router.post("/request")
def create_booking_request(booking_request: BookingRequestRequest, db: db_dep):
    integration_id = booking_request.integration_id
    restaurant = db.query(models.Integrations).filter(
        models.Integrations.id == integration_id).first().restaurant
    new_booking = BookingRequest(integration_id=integration_id, restaurant=restaurant,
                                 num_persons=booking_request.num_persons, time=booking_request.time,
                                 extra_parameters=booking_request.extra_parameters,
                                 created=datetime.datetime.utcnow())
    new_booking_str = json.dumps(new_booking, cls=BookingRequest.BookingRequestEncoder)
    new_booking_request_data = new_booking_str.encode("utf-8")
    print(f"Publish {new_booking_request_data}.")
    future = publisher.publish(topic_path, new_booking_request_data)
    # TODO handle cancelled? See subscriber
    future.result()


# TODO: May be needed?
# @router.delete("/request/{id}", status_code=204)
# def delete_booking_request(id: int = Path(gt=0)):
#    if BOOKING_REQUESTS.get(id) is None:
#        raise HTTPException(status_code=404)
#    BOOKING_REQUESTS.pop(id)


# TODO: Probably not valid/needed
# @router.put("/{id}")
# def update_booking(id : int, booking_update : bookingreq, db = db_dep):
#    booking_to_update = db.query(models.Bookings).all().filter(models.Bookings.id == id).first()
#    if booking_to_update is None:
#        raise HTTPException(status_code=404)
#    booking_to_update.restaurant = bookingreq.restaurant
#    booking_to_update.time = bookingreq.time

#    db.add(booking_to_update)
#    db.commit()


@router.get("/{id}", status_code=200)
def get_booking_by_id(db: db_dep, id: int = Path(gt=0)):
    matching_booking = db.query(models.Bookings).all().filter(models.Bookings.id == id).first()
    if matching_booking is None:
        raise HTTPException(status_code=404)
    return matching_booking
