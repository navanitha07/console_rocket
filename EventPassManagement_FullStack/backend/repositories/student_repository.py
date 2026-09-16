from sqlalchemy.orm import Session
from models.student import Student


def create(db: Session, data):
    obj = Student(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_all(db: Session):
    return db.query(Student).order_by(Student.stu_id).all()


def get_by_id(db: Session, stu_id: int):
    return db.get(Student, stu_id)


def update(db: Session, obj: Student, data):
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj: Student):
    db.delete(obj)
    db.commit()
