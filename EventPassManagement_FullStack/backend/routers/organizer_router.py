from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas import OrganizerCreate, OrganizerOut
from services import organizer_service

router = APIRouter(prefix="/api/organizers", tags=["Organizers"])


@router.post("", response_model=OrganizerOut)
def create_organizer(
    data: OrganizerCreate,
    db: Session = Depends(get_db),
):
    return organizer_service.create(db, data)


@router.get("", response_model=list[OrganizerOut])
def get_organizers(db: Session = Depends(get_db)):
    return organizer_service.get_all(db)


@router.get("/{organizer_id}", response_model=OrganizerOut)
def get_organizer(
    organizer_id: int,
    db: Session = Depends(get_db),
):
    return organizer_service.get_by_id(db, organizer_id)


@router.put("/{organizer_id}", response_model=OrganizerOut)
def update_organizer(
    organizer_id: int,
    data: OrganizerCreate,
    db: Session = Depends(get_db),
):
    return organizer_service.update(db, organizer_id, data)


@router.delete("/{organizer_id}")
def delete_organizer(
    organizer_id: int,
    db: Session = Depends(get_db),
):
    organizer_service.delete(db, organizer_id)
    return {"message": "Organizer deleted"}
