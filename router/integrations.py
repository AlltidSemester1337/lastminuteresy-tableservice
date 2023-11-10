from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from integration import IntegrationRequest, Integration

router = APIRouter(
    prefix="/integrations",
    tags=["integrations"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dep = Annotated[Session, Depends(get_db)]


@router.get("/by_restaurant")
def get_all_integrations_by_restaurant(db: db_dep, restaurant_name: str = Query(min_length=2, max_length=100)):
    return db.query(models.Integrations).filter(
        models.Integrations.restaurant == restaurant_name).all()


@router.get("/")
def get_all_integrations(db: db_dep):
    return db.query(models.Integrations).all()


@router.delete("/{id}", status_code=204)
def delete_integration(db: db_dep, id: int = Path(gt=-1)):
    db.query(models.Integrations).filter(models.Integrations.id == id).delete()
    db.commit()


@router.post("/", status_code=201)
def create_booking_request(new_integration_request: IntegrationRequest, db: db_dep):
    new_integration = models.Integrations(**new_integration_request.model_dump())
    db.add(new_integration)
    db.commit()
