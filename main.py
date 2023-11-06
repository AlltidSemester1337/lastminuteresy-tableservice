from fastapi import FastAPI, Path, Query, HTTPException
from booking import Booking
from bookingrequest import BookingRequest, BookingRequestRequest

app = FastAPI()

# TODO example data to test
FREE_BOOKINGS = {1: Booking(1, "McDonalds", "1970-01-01:19:30:00"),
                 2: Booking(2, "Lökens restaurang", "1970-01-01:19:30:00")}

BOOKING_REQUESTS = {}

ID_GENERATOR = iter(range(1, 1000))


@app.get("/bookings/free/all")
def get_all_free_bookings():
    return FREE_BOOKINGS


@app.get("/bookings/free")
def get_all_free_bookings_by_name(restaurant_name: str = Query(min_length=2, max_length=100)):
    return [booking for booking in FREE_BOOKINGS.values() if
            booking.restaurant.casefold() == restaurant_name.casefold()]


@app.get("/bookings/request")
def get_active_booking_requests():
    return BOOKING_REQUESTS


@app.post("/bookings/request", status_code=201)
def create_booking_request(booking_request: BookingRequestRequest):
    new_booking = BookingRequest(**booking_request.model_dump())
    num_bookings = len(BOOKING_REQUESTS)
    new_booking.id = 0 if num_bookings == 0 else num_bookings
    BOOKING_REQUESTS[new_booking.id] = new_booking


@app.delete("/bookings/request/{id}", status_code=204)
def delete_booking_request(id: int = Path(gt = 0)):
    if BOOKING_REQUESTS.get(id) is None:
        raise HTTPException(status_code = 404)
    BOOKING_REQUESTS.pop(id)


# TODO: Probably not valid/needed
# @app.put("/bookings/{id}")
# def update_booking(id : int, booking_update=Body()):
#    if FREE_BOOKINGS[id] is None:
#        return None
#    FREE_BOOKINGS[id] = booking_update
#    return FREE_BOOKINGS[id]


@app.get("/bookings/{id}", status_code=200)
def get_booking_by_id(id: int = Path(gt = 0)):
    if FREE_BOOKINGS.get(id) is None:
        raise HTTPException(status_code=404)
    return FREE_BOOKINGS.get(id)
