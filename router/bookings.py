import datetime
from typing import Annotated

from fastapi import APIRouter, Path, Query, HTTPException, Depends
from sqlalchemy.orm import Session

from booking import Booking
from bookingrequest import BookingRequest, BookingRequestRequest
from database import SessionLocal
import models

router = APIRouter()

# TODO example data to test
FREE_BOOKINGS = {1: Booking(1, "McDonalds", "1970-01-01:19:30:00"),
                 2: Booking(2, "Lökens restaurang", "1970-01-01:19:30:00")}

BOOKING_REQUESTS = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dep = Annotated[Session, Depends(get_db)]


@router.get("/bookings/free/all")
def get_all_free_bookings(db: db_dep):
    return db.query(models.Bookings).all()


@router.get("/bookings/free")
def get_all_free_bookings_by_name(db: db_dep, restaurant_name: str = Query(min_length=2, max_length=100)):
    return db.query(models.Bookings).all().filter(models.Bookings.restaurant.casefold() == restaurant_name.casefold())


@router.delete("/bookings/{id}", status_code=204)
def delete_booking_request(id: int = Path(gt=0), db=db_dep):
    db.query(models.Bookings).filter(models.Bookings.id == id).delete()


@router.get("/bookings/request")
def get_active_booking_requests():
    return BOOKING_REQUESTS


@router.post("/bookings/request", status_code=201)
def create_booking_request(booking_request: BookingRequestRequest):
    new_booking = BookingRequest(**booking_request.model_dump())
    num_bookings = len(BOOKING_REQUESTS)
    new_booking.id = 0 if num_bookings == 0 else num_bookings
    BOOKING_REQUESTS[new_booking.id] = new_booking


@router.delete("/bookings/request/{id}", status_code=204)
def delete_booking_request(id: int = Path(gt=0)):
    if BOOKING_REQUESTS.get(id) is None:
        raise HTTPException(status_code=404)
    BOOKING_REQUESTS.pop(id)


# TODO: Probably not valid/needed
# @router.put("/bookings/{id}")
# def update_booking(id : int, booking_update : bookingreq, db = db_dep):
#    booking_to_update = db.query(models.Bookings).all().filter(models.Bookings.id == id).first()
#    if booking_to_update is None:
#        raise HTTPException(status_code=404)
#    booking_to_update.restaurant = bookingreq.restaurant
#    booking_to_update.time = bookingreq.time

#    db.add(booking_to_update)
#    db.commit()


@router.get("/bookings/{id}", status_code=200)
def get_booking_by_id(db: db_dep, id: int = Path(gt=0)):
    matching_booking = db.query(models.Bookings).all().filter(models.Bookings.id == id).first()
    if matching_booking is None:
        raise HTTPException(status_code=404)
    return matching_booking
