from pathlib import Path
import sqlite3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from database.connection import Base, engine
import models  # noqa: F401
from routers import (
    student_router,
    organizer_router,
    event_router,
    registration_router,
    report_router,
)

BASE_DIR = Path(__file__).resolve().parent
STARTUP_SQL = BASE_DIR / "startup.sql"
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(
    title="Event Pass Management System",
    version="1.0.0",
    description="Event registration application based strictly on the supplied ER diagram.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)

app.include_router(student_router.router)
app.include_router(organizer_router.router)
app.include_router(event_router.router)
app.include_router(registration_router.router)
app.include_router(report_router.router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

    db_path = BASE_DIR / "event_pass.db"
    with sqlite3.connect(db_path) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM organizers"
        ).fetchone()[0]

        if count == 0:
            conn.executescript(
                STARTUP_SQL.read_text(encoding="utf-8")
            )
            conn.commit()


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND_DIR / "index.html")
