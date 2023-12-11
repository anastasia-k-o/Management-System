from sqlalchemy import Column, Date, Time, DateTime, ForeignKey, Integer, String, Table

from nto.models.meta import meta

event_types_table = Table(
    "event_types",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
)

events_table = Table(
    "events",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("date", Date),
    Column("description", String),
    Column("event_type_id", ForeignKey("event_types.id", ondelete="RESTRICT")),
)

labor_types_table = Table(
    "labor_types",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
)

rooms_table = Table(
    "rooms",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
    Column("events_number", Integer, default=0)

)

labor_requests_table = Table(
    "labor_requests",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
    Column("registration_date", Date),
    Column("deadline_date", Date),  # не уверен, что это дата
    Column("description", String),
    Column("status", Integer),
    Column("room_id", ForeignKey("rooms.id", ondelete="RESTRICT")),
    Column("event_id", ForeignKey("events.id", ondelete="RESTRICT")),
    Column("labor_type_id", ForeignKey("labor_types.id", ondelete="RESTRICT")),

)

booking_table = Table(
    "booking",
    meta,
    Column("date_registration", Date),
    Column("id", Integer, primary_key=True),
    Column("room_id", ForeignKey("rooms.id", ondelete="RESTRICT")),
    Column("event_id", ForeignKey("events.id", ondelete="RESTRICT")),
    Column("date_start", DateTime),
    Column("date_end", DateTime),
    Column("description", String),
    Column("booking_part", Integer)

)

classes_type_table = Table(
    "classes_type",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
)

teachers_table = Table(
    "teachers",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
)
week_days_table = Table(
    "week_days",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
)

classes_table = Table(
    "classes",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
    Column("date_start", Date),
    Column("class_id", ForeignKey("classes_type.id", ondelete="RESTRICT")),
    Column("teacher_id", ForeignKey("teachers.id", ondelete="RESTRICT")),
    Column("room_id", ForeignKey("rooms.id", ondelete="RESTRICT")),
    Column("class_time", Integer),
    Column("class_day1", ForeignKey("week_days.id", ondelete="RESTRICT"), nullable=True),
    Column("class_day2", ForeignKey("week_days.id", ondelete="RESTRICT"), nullable=True),
    Column("class_day3", ForeignKey("week_days.id", ondelete="RESTRICT"), nullable=True),
    Column("class_start", Time),
    Column("class_end", Time)
)
