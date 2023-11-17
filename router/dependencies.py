from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()