from router import bookings
from fastapi import FastAPI
import models
from database import engine

app = FastAPI()
app.include_router(bookings.router)

models.Base.metadata.create_all(bind=engine)
