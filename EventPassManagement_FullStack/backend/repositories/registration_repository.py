from sqlalchemy.orm import Session
from models.registration import Registration


def create(db: Session, data):
    obj = Registration(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_all(db: Session):
    return (
        db.query(Registration)
        .order_by(Registration.registration_id)
        .all()
    )


def get_by_id(db: Session, registration_id: int):
    return db.get(Registration, registration_id)


def get_by_student_event(db: Session, stu_id: int, event_id: int):
    return (
        db.query(Registration)
        .filter(
            Registration.stu_id == stu_id,
            Registration.event_id == event_id,
        )
        .first()
    )


def update(db: Session, obj: Registration, data):
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj: Registration):
    db.delete(obj)
    db.commit()
