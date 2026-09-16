from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from repositories import (
    registration_repository,
    student_repository,
    event_repository,
)


def create(db, data):
    if not student_repository.get_by_id(db, data.stu_id):
        raise HTTPException(400, "Student does not exist")

    event = event_repository.get_by_id(db, data.event_id)
    if not event:
        raise HTTPException(400, "Event does not exist")

    if event.status.lower() != "open":
        raise HTTPException(400, "Registration is closed for this event")

    existing = registration_repository.get_by_student_event(
        db, data.stu_id, data.event_id
    )

    if existing and existing.status != "CANCELLED":
        raise HTTPException(
            400,
            "Student is already registered for this event",
        )

    count = event_repository.registration_count(db, data.event_id)
    if count >= event.maximum_capacity:
        raise HTTPException(400, "Event capacity is full")

    if existing and existing.status == "CANCELLED":
        existing.status = "REGISTERED"
        existing.check_in_time = None
        existing.check_out_time = None
        db.commit()
        db.refresh(existing)
        return existing

    try:
        return registration_repository.create(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            400,
            "Duplicate registration is not allowed",
        )


def get_all(db):
    return registration_repository.get_all(db)


def get_by_id(db, registration_id):
    obj = registration_repository.get_by_id(db, registration_id)
    if not obj:
        raise HTTPException(404, "Registration not found")
    return obj


def update(db, registration_id, data):
    obj = get_by_id(db, registration_id)

    if not student_repository.get_by_id(db, data.stu_id):
        raise HTTPException(400, "Student does not exist")

    if not event_repository.get_by_id(db, data.event_id):
        raise HTTPException(400, "Event does not exist")

    duplicate = registration_repository.get_by_student_event(
        db, data.stu_id, data.event_id
    )
    if duplicate and duplicate.registration_id != registration_id:
        raise HTTPException(
            400,
            "That student is already registered for this event",
        )

    return registration_repository.update(db, obj, data)


def delete(db, registration_id):
    obj = get_by_id(db, registration_id)
    registration_repository.delete(db, obj)


def cancel(db, registration_id):
    obj = get_by_id(db, registration_id)
    event = event_repository.get_by_id(db, obj.event_id)

    if datetime.now() >= event.event_date:
        raise HTTPException(
            400,
            "Registration cannot be cancelled after the event date",
        )

    if obj.status == "CANCELLED":
        raise HTTPException(400, "Registration is already cancelled")

    obj.status = "CANCELLED"
    obj.check_in_time = None
    obj.check_out_time = None
    db.commit()
    db.refresh(obj)
    return obj


def check_in(db, registration_id):
    obj = get_by_id(db, registration_id)
    event = event_repository.get_by_id(db, obj.event_id)

    if obj.status == "CANCELLED":
        raise HTTPException(
            400,
            "Cancelled registration cannot check in",
        )

    if obj.check_in_time is not None or obj.status == "CHECKED_IN":
        raise HTTPException(
            400,
            "Check-in is allowed only once",
        )

    if datetime.now().date() != event.event_date.date():
        raise HTTPException(
            400,
            "Check-in is allowed only on the event day",
        )

    obj.check_in_time = datetime.now()
    obj.status = "CHECKED_IN"
    db.commit()
    db.refresh(obj)
    return obj
