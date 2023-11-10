from router import bookings, integrations
from fastapi import FastAPI
import models
from database import engine

app = FastAPI()
app.include_router(bookings.router)
app.include_router(integrations.router)

models.Base.metadata.create_all(bind=engine)
