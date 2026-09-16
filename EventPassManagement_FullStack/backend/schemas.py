from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class OrganizerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class OrganizerOut(OrganizerCreate):
    organizer_id: int
    model_config = ConfigDict(from_attributes=True)


class StudentCreate(BaseModel):
    stu_name: str = Field(min_length=1, max_length=100)
    department: str | None = None
    phone_no: str | None = None


class StudentOut(StudentCreate):
    stu_id: int
    model_config = ConfigDict(from_attributes=True)


class EventCreate(BaseModel):
    event_name: str = Field(min_length=1, max_length=150)
    organizer_id: int
    maximum_capacity: int = Field(gt=0)
    status: str = "Open"
    event_date: datetime
    start_time: str | None = None
    end_time: str | None = None


class EventOut(EventCreate):
    event_id: int
    model_config = ConfigDict(from_attributes=True)


class RegistrationCreate(BaseModel):
    stu_id: int
    event_id: int
    status: str = "REGISTERED"


class RegistrationOut(BaseModel):
    registration_id: int
    stu_id: int
    event_id: int
    check_in_time: datetime | None
    check_out_time: datetime | None
    status: str
    model_config = ConfigDict(from_attributes=True)
