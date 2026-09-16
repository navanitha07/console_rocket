# EventPassManagement_FullStack

Event Pass Management System built strictly from the supplied ER diagram.

## ER entities

- Student
- Organizer
- Event
- Registration

No login/user/payment/pass entity has been added.

## Architecture

```text
EventPassManagement_FullStack/
│
├── backend/
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── student.py
│   │   ├── organizer.py
│   │   ├── event.py
│   │   └── registration.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── student_repository.py
│   │   ├── organizer_repository.py
│   │   ├── event_repository.py
│   │   └── registration_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── student_service.py
│   │   ├── organizer_service.py
│   │   ├── event_service.py
│   │   └── registration_service.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── student_router.py
│   │   ├── organizer_router.py
│   │   ├── event_router.py
│   │   ├── registration_router.py
│   │   └── report_router.py
│   ├── schemas.py
│   ├── startup.sql
│   ├── requirements.txt
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── .gitignore
└── README.md
```

## Run backend

Windows:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Linux/macOS:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

The SQLite database is created automatically and `startup.sql` loads initial data on first startup.

## Main APIs

### Student
- POST `/api/students`
- GET `/api/students`
- GET `/api/students/{stu_id}`
- PUT `/api/students/{stu_id}`
- DELETE `/api/students/{stu_id}`

### Organizer
- POST `/api/organizers`
- GET `/api/organizers`
- GET `/api/organizers/{organizer_id}`
- PUT `/api/organizers/{organizer_id}`
- DELETE `/api/organizers/{organizer_id}`

### Event
- POST `/api/events`
- GET `/api/events`
- GET `/api/events/{event_id}`
- PUT `/api/events/{event_id}`
- DELETE `/api/events/{event_id}`
- GET `/api/events/summary`
- GET `/api/events/highest-registrations`

### Registration
- POST `/api/registrations`
- GET `/api/registrations`
- GET `/api/registrations/{registration_id}`
- PUT `/api/registrations/{registration_id}`
- DELETE `/api/registrations/{registration_id}`
- POST `/api/registrations/{registration_id}/cancel`
- POST `/api/registrations/{registration_id}/check-in`

## Business rules

- A student can register once for an event.
- Registration is blocked when capacity is full.
- Cancelled registrations release capacity.
- Cancellation is allowed before the event date.
- Only registered students can check in.
- Check-in is allowed only on the event day.
- Check-in can happen only once.
- Event summary shows capacity, registered count and checked-in count.
- Highest-registration report is sorted descending.

## GitHub

The repository intentionally excludes:
- virtual environments
- Python cache
- SQLite database
- IDE settings

So it is clean to clone/fetch and run.
