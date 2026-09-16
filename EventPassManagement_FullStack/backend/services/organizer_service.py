from fastapi import HTTPException
from models.event import Event
from repositories import organizer_repository


def create(db, data):
    return organizer_repository.create(db, data)


def get_all(db):
    return organizer_repository.get_all(db)


def get_by_id(db, organizer_id):
    obj = organizer_repository.get_by_id(db, organizer_id)
    if not obj:
        raise HTTPException(404, "Organizer not found")
    return obj


def update(db, organizer_id, data):
    obj = get_by_id(db, organizer_id)
    return organizer_repository.update(db, obj, data)


def delete(db, organizer_id):
    obj = get_by_id(db, organizer_id)
    if db.query(Event).filter(Event.organizer_id == organizer_id).first():
        raise HTTPException(400, "Organizer has events and cannot be deleted")
    organizer_repository.delete(db, obj)
