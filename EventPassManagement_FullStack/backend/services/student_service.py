from fastapi import HTTPException
from repositories import student_repository


def create(db, data):
    return student_repository.create(db, data)


def get_all(db):
    return student_repository.get_all(db)


def get_by_id(db, stu_id):
    obj = student_repository.get_by_id(db, stu_id)
    if not obj:
        raise HTTPException(404, "Student not found")
    return obj


def update(db, stu_id, data):
    obj = get_by_id(db, stu_id)
    return student_repository.update(db, obj, data)


def delete(db, stu_id):
    obj = get_by_id(db, stu_id)
    student_repository.delete(db, obj)
