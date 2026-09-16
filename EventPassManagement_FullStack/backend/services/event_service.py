from fastapi import HTTPException
from repositories import event_repository, organizer_repository


def create(db, data):
    if not organizer_repository.get_by_id(db, data.organizer_id):
        raise HTTPException(400, "Organizer does not exist")
    return event_repository.create(db, data)


def get_all(db):
    return event_repository.get_all(db)


def get_by_id(db, event_id):
    obj = event_repository.get_by_id(db, event_id)
    if not obj:
        raise HTTPException(404, "Event not found")
    return obj


def update(db, event_id, data):
    obj = get_by_id(db, event_id)
    if not organizer_repository.get_by_id(db, data.organizer_id):
        raise HTTPException(400, "Organizer does not exist")

    current_count = event_repository.registration_count(db, event_id)
    if data.maximum_capacity < current_count:
        raise HTTPException(
            400,
            f"Capacity cannot be below current registrations ({current_count})",
        )

    return event_repository.update(db, obj, data)


def delete(db, event_id):
    obj = get_by_id(db, event_id)
    event_repository.delete(db, obj)


def summary(db):
    result = []
    for event in get_all(db):
        result.append({
            "event_id": event.event_id,
            "event_name": event.event_name,
            "capacity": event.maximum_capacity,
            "registered_count": event_repository.registration_count(
                db, event.event_id
            ),
            "checked_in_count": event_repository.checked_in_count(
                db, event.event_id
            ),
            "status": event.status,
            "event_date": event.event_date,
        })
    return result


def highest_registrations(db):
    return sorted(
        summary(db),
        key=lambda item: item["registered_count"],
        reverse=True,
    )
