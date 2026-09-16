from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from services import event_service

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/event-registrations")
def event_registrations(db: Session = Depends(get_db)):
    return event_service.highest_registrations(db)
