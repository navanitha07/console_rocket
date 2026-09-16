from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas import RegistrationCreate, RegistrationOut
from services import registration_service

router = APIRouter(
    prefix="/api/registrations",
    tags=["Registrations"],
)


@router.post("", response_model=RegistrationOut)
def create_registration(
    data: RegistrationCreate,
    db: Session = Depends(get_db),
):
    return registration_service.create(db, data)


@router.get("", response_model=list[RegistrationOut])
def get_registrations(db: Session = Depends(get_db)):
    return registration_service.get_all(db)


@router.get(
    "/{registration_id}",
    response_model=RegistrationOut,
)
def get_registration(
    registration_id: int,
    db: Session = Depends(get_db),
):
    return registration_service.get_by_id(db, registration_id)


@router.put(
    "/{registration_id}",
    response_model=RegistrationOut,
)
def update_registration(
    registration_id: int,
    data: RegistrationCreate,
    db: Session = Depends(get_db),
):
    return registration_service.update(db, registration_id, data)


@router.delete("/{registration_id}")
def delete_registration(
    registration_id: int,
    db: Session = Depends(get_db),
):
    registration_service.delete(db, registration_id)
    return {"message": "Registration deleted"}


@router.post(
    "/{registration_id}/cancel",
    response_model=RegistrationOut,
)
def cancel_registration(
    registration_id: int,
    db: Session = Depends(get_db),
):
    return registration_service.cancel(db, registration_id)


@router.post(
    "/{registration_id}/check-in",
    response_model=RegistrationOut,
)
def check_in(
    registration_id: int,
    db: Session = Depends(get_db),
):
    return registration_service.check_in(db, registration_id)
