import datetime
from typing import Annotated

from fastapi import APIRouter, Path, Query, HTTPException, Depends
from sqlalchemy.orm import Session

from bookingrequest import BookingRequest, BookingRequestRequest
from database import SessionLocal
import models
from google.cloud import pubsub_v1
import json

project_id = "sapient-bucksaw-401016"
topic_id = "booking-requests"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

router = APIRouter(
    prefix="/bookings"
)

BOOKING_REQUESTS = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dep = Annotated[Session, Depends(get_db)]


@router.get("/free/all")
def get_all_free_bookings(db: db_dep):
    return db.query(models.Bookings).all()


@router.get("/free")
def get_all_free_bookings_by_name(db: db_dep, restaurant_name: str = Query(min_length=2, max_length=100)):
    return db.query(models.Bookings).all().filter(models.Bookings.restaurant.casefold() == restaurant_name.casefold())


@router.delete("/{id}", status_code=204)
def delete_booking_request(id: int = Path(gt=-1), db=db_dep):
    db.query(models.Bookings).filter(models.Bookings.id == id).delete()


@router.get("/request")
def get_active_booking_requests():
    return BOOKING_REQUESTS


@router.post("/request")
def create_booking_request(booking_request: BookingRequestRequest):
    new_booking = BookingRequest(**booking_request.model_dump(), created = datetime.datetime.utcnow())
    new_booking_str = json.dumps(new_booking, cls=BookingRequest.BookingRequestEncoder)
    new_booking_data = new_booking_str.encode("utf-8")
    future = publisher.publish(topic_path, new_booking_data)
    future.result()


@router.delete("/request/{id}", status_code=204)
def delete_booking_request(id: int = Path(gt=0)):
    if BOOKING_REQUESTS.get(id) is None:
        raise HTTPException(status_code=404)
    BOOKING_REQUESTS.pop(id)


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
