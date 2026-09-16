from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.connection import Base


class Organizer(Base):
    __tablename__ = "organizers"

    organizer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    events = relationship("Event", back_populates="organizer")
