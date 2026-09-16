from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas import StudentCreate, StudentOut
from services import student_service

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.post("", response_model=StudentOut)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    return student_service.create(db, data)


@router.get("", response_model=list[StudentOut])
def get_students(db: Session = Depends(get_db)):
    return student_service.get_all(db)


@router.get("/{stu_id}", response_model=StudentOut)
def get_student(stu_id: int, db: Session = Depends(get_db)):
    return student_service.get_by_id(db, stu_id)


@router.put("/{stu_id}", response_model=StudentOut)
def update_student(
    stu_id: int,
    data: StudentCreate,
    db: Session = Depends(get_db),
):
    return student_service.update(db, stu_id, data)


@router.delete("/{stu_id}")
def delete_student(stu_id: int, db: Session = Depends(get_db)):
    student_service.delete(db, stu_id)
    return {"message": "Student deleted"}
