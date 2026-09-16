from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(150), nullable=False)
    organizer_id = Column(
        Integer,
        ForeignKey("organizers.organizer_id"),
        nullable=False,
    )
    maximum_capacity = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="Open")
    event_date = Column(DateTime, nullable=False)
    start_time = Column(String(10))
    end_time = Column(String(10))

    organizer = relationship("Organizer", back_populates="events")
    registrations = relationship(
        "Registration",
        back_populates="event",
        cascade="all, delete-orphan",
    )
