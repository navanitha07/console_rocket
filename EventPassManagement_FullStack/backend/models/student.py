from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.connection import Base


class Student(Base):
    __tablename__ = "students"

    stu_id = Column(Integer, primary_key=True, index=True)
    stu_name = Column(String(100), nullable=False)
    department = Column(String(100))
    phone_no = Column(String(20))

    registrations = relationship(
        "Registration",
        back_populates="student",
        cascade="all, delete-orphan",
    )
