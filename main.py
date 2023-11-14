import datetime
import json
from contextlib import contextmanager

from google.cloud import pubsub_v1
from sqlalchemy.orm import Session

from router import bookings, integrations
from fastapi import FastAPI
import models
from database import engine, SessionLocal
import threading
import asyncio
from concurrent.futures import TimeoutError

app = FastAPI()
app.include_router(bookings.router)
app.include_router(integrations.router)

models.Base.metadata.create_all(bind=engine)

project_id = "sapient-bucksaw-401016"
subscription_id = "bookings-sub"
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


@contextmanager
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    pubsub_thread = threading.Thread(target=run_pubsub_subscriber, daemon=True)
    pubsub_thread.start()


def run_pubsub_subscriber():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(subscribe())


async def subscribe():

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message}.")
        message_data_json = json.loads(message.data)
        message_data_json["time"] = datetime.datetime.fromisoformat(message_data_json["time"])
        new_booking = models.Bookings(restaurant=message_data_json["restaurant"], time=message_data_json["time"])
        # Use the get_db context manager
        with get_db() as db:
            db.add(new_booking)
            db.commit()
            message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely TODO might be a problem? Should be owned / close when main thread shuts down
            await streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            await streaming_pull_future.result()  # Block until the shutdown is complete.
