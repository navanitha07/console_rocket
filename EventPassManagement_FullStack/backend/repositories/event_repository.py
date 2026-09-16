from sqlalchemy import func
from sqlalchemy.orm import Session
from models.event import Event
from models.registration import Registration


def create(db: Session, data):
    obj = Event(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_all(db: Session):
    return db.query(Event).order_by(Event.event_date).all()


def get_by_id(db: Session, event_id: int):
    return db.get(Event, event_id)


def update(db: Session, obj: Event, data):
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj: Event):
    db.delete(obj)
    db.commit()


def registration_count(db: Session, event_id: int):
    return (
        db.query(func.count(Registration.registration_id))
        .filter(
            Registration.event_id == event_id,
            Registration.status.in_(["REGISTERED", "CHECKED_IN"]),
        )
        .scalar()
    )


def checked_in_count(db: Session, event_id: int):
    return (
        db.query(func.count(Registration.registration_id))
        .filter(
            Registration.event_id == event_id,
            Registration.status == "CHECKED_IN",
        )
        .scalar()
    )
