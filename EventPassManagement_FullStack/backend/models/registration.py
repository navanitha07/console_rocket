from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from database.connection import Base


class Registration(Base):
    __tablename__ = "registrations"

    __table_args__ = (
        UniqueConstraint(
            "stu_id",
            "event_id",
            name="uq_student_event",
        ),
    )

    registration_id = Column(Integer, primary_key=True, index=True)
    stu_id = Column(
        Integer,
        ForeignKey("students.stu_id"),
        nullable=False,
    )
    event_id = Column(
        Integer,
        ForeignKey("events.event_id"),
        nullable=False,
    )
    check_in_time = Column(DateTime)
    check_out_time = Column(DateTime)
    status = Column(String(20), nullable=False, default="REGISTERED")

    student = relationship("Student", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")
