from sqlalchemy.orm import Session
from models.organizer import Organizer


def create(db: Session, data):
    obj = Organizer(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_all(db: Session):
    return db.query(Organizer).order_by(Organizer.organizer_id).all()


def get_by_id(db: Session, organizer_id: int):
    return db.get(Organizer, organizer_id)


def update(db: Session, obj: Organizer, data):
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj: Organizer):
    db.delete(obj)
    db.commit()
