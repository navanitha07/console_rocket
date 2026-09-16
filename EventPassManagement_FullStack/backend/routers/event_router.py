from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas import EventCreate, EventOut
from services import event_service

router = APIRouter(prefix="/api/events", tags=["Events"])


@router.get("/summary")
def event_summary(db: Session = Depends(get_db)):
    return event_service.summary(db)


@router.get("/highest-registrations")
def highest_registrations(db: Session = Depends(get_db)):
    return event_service.highest_registrations(db)


@router.post("", response_model=EventOut)
def create_event(data: EventCreate, db: Session = Depends(get_db)):
    return event_service.create(db, data)


@router.get("", response_model=list[EventOut])
def get_events(db: Session = Depends(get_db)):
    return event_service.get_all(db)


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    return event_service.get_by_id(db, event_id)


@router.put("/{event_id}", response_model=EventOut)
def update_event(
    event_id: int,
    data: EventCreate,
    db: Session = Depends(get_db),
):
    return event_service.update(db, event_id, data)


@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event_service.delete(db, event_id)
    return {"message": "Event deleted"}
