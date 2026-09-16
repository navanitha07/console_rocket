PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS organizers (
    organizer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    stu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stu_name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    phone_no VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name VARCHAR(150) NOT NULL,
    organizer_id INTEGER NOT NULL,
    maximum_capacity INTEGER NOT NULL CHECK (maximum_capacity > 0),
    status VARCHAR(20) NOT NULL DEFAULT 'Open',
    event_date DATETIME NOT NULL,
    start_time VARCHAR(10),
    end_time VARCHAR(10),
    FOREIGN KEY (organizer_id) REFERENCES organizers(organizer_id)
);

CREATE TABLE IF NOT EXISTS registrations (
    registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stu_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    check_in_time DATETIME,
    check_out_time DATETIME,
    status VARCHAR(20) NOT NULL DEFAULT 'REGISTERED',
    FOREIGN KEY (stu_id) REFERENCES students(stu_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    CONSTRAINT uq_student_event UNIQUE (stu_id, event_id)
);

CREATE INDEX IF NOT EXISTS idx_registration_event
ON registrations(event_id);

CREATE INDEX IF NOT EXISTS idx_registration_student
ON registrations(stu_id);

INSERT OR IGNORE INTO organizers (organizer_id, name) VALUES
    (1, 'Tech Club'),
    (2, 'Computer Science Association');

INSERT OR IGNORE INTO students
(stu_id, stu_name, department, phone_no) VALUES
    (1, 'Ananya', 'Information Technology', '9876543210'),
    (2, 'Rahul', 'Computer Science', '9876543211'),
    (3, 'Priya', 'Information Technology', '9876543212'),
    (4, 'Arun', 'Electronics', '9876543213'),
    (5, 'Meena', 'Computer Science', '9876543214');

INSERT OR IGNORE INTO events
(event_id, event_name, organizer_id, maximum_capacity, status,
 event_date, start_time, end_time) VALUES
    (1, 'AI & Future Tech', 1, 100, 'Open',
     '2026-10-10 00:00:00', '10:00', '13:00'),
    (2, 'Hackathon 2026', 2, 50, 'Open',
     '2026-10-18 00:00:00', '09:00', '18:00'),
    (3, 'Cloud Computing Workshop', 1, 40, 'Open',
     '2026-10-25 00:00:00', '14:00', '17:00');

INSERT OR IGNORE INTO registrations
(registration_id, stu_id, event_id, status) VALUES
    (1, 1, 1, 'REGISTERED'),
    (2, 2, 1, 'REGISTERED'),
    (3, 3, 1, 'CHECKED_IN'),
    (4, 4, 2, 'REGISTERED'),
    (5, 5, 2, 'REGISTERED');
