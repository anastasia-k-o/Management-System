import os
from datetime import date, datetime

from sqlalchemy import create_engine, insert, text

from nto.models.meta import meta
from nto.models.tables import (
    event_types_table,
    events_table,
    labor_requests_table,
    labor_types_table,
    rooms_table, booking_table, classes_type_table, week_days_table, teachers_table,
)
from nto.utils.get_path import get_appdata

engine = create_engine(
    "sqlite:///{}".format(get_appdata("database.db")),
    echo=True,
)
meta.create_all(bind=engine)

conn = engine.connect()


def fill_initial_data() -> None:
    conn.execute(text("PRAGMA foreign_keys = ON"))

    _initial_event_types = [
        {"name": "Спектакль"},
        {"name": "Концерт"},
        {"name": "Репетиция"},
        {"name": "Выставка"},
    ]

    _initial_events = [
        {
            "name": "Кошкин дом",
            "date": date(2023, 11, 25),
            "description": """
            Спектакль Детского музыкального театра "Город мастеров"
 по одноименной сказке С. Маршака на музыку Н. Александровой
            """.replace(
                "\n", ""
            ).strip(),
            "event_type_id": 1,
        },
        {
            "name": "Ад - это другие",
            "date": date(2023, 11, 26),
            "description": """
            Спектакль театра-студии "Первая сцена"
 по пьесе Ж.-П. Сартра "За закрытыми дверями"
            """.replace(
                "\n", ""
            ).strip(),
            "event_type_id": 1,
        },
    ]

    _initial_rooms = [
        {
            "name": "Колонный зал",

        },
        {
            "name": "Большой зал",
            "events_number":1
        },
        {
            "name": "Зал-конструктор",
            "events_number":1
        },
        {
            "name": "Малый зал",
        },
        {
            "name": "Лекторий",
        },
        {
            "name": "Библиотека",
            "events_number":1
        },
        {
            "name": "Зимний сад",
        },
    ]

    _initial_labor_types = [
        {
            "name": "Приготовить реквизит",
        },
        {
            "name": "Установить декорации",
        },
        {
            "name": "Настроить освещение",
        },
        {
            "name": "Настроить музыкальное сопровождение",
        },
    ]

    _initial_labor_requests = [
        {
            "name": "Декорации для Города мастеров",
            "labor_type_id": 2,
            "room_id": 2,
            "event_id": 1,
            "deadline_date": date(2023, 11, 23),
            "registration_date": date(2023, 11, 20),
            "status": 2,
            "description": "Установить декорации в сказочном стиле",
        },
        {
            "name": "Реквизит для Города мастеров",
            "labor_type_id": 1,
            "room_id": 2,
            "event_id": 1,
            "deadline_date": date(2023, 11, 22),
            "registration_date": date(2023, 11, 20),
            "status": 2,
            "description": "",
        },
        {
            "name": "Музыкальное сопровождение для Города мастеров",
            "labor_type_id": 3,
            "room_id": 2,
            "event_id": 1,
            "deadline_date": date(2023, 11, 24),
            "registration_date": date(2023, 11, 23),
            "status": 0,
            "description": 'Запросить элементы музыкального сопровождения у коллектива "Город мастеров", затем настроить',
        },
        {
            "name": "Освещение в малом зале",
            "labor_type_id": 4,
            "room_id": 4,
            "event_id": 2,
            "deadline_date": date(2023, 11, 25),
            "registration_date": date(2023, 11, 21),
            "status": 1,
            "description": "",
        },
        {
            "name": "Декорации для Первой сцены",
            "labor_type_id": 2,
            "room_id": 4,
            "event_id": 2,
            "deadline_date": date(2023, 11, 24),
            "registration_date": date(2023, 11, 21),
            "status": 1,
            "description": 'Расставить декорации для коллектива "Первая сцена"',
        },
        {
            "name": "Реквизит для Первой сцены",
            "labor_type_id": 1,
            "room_id": 4,
            "event_id": 2,
            "deadline_date": date(2023, 11, 25),
            "registration_date": date(2023, 11, 24),
            "status": 0,
            "description": "",
        },
    ]

    _initial_booking = [
        {
            "date_registration":date(2023,11,20),
            "room_id": 2,
            "event_id": 1,
            "date_start": datetime(2023, 11, 20,14,00,00),
            "date_end": datetime(2023, 11, 23,18,00,00),
            "booking_part":1,
            "description": "Установить декорации в сказочном стиле",
        },

    ]

    _initial_week_days = [
        {"name" : "Понедельник"},
        {"name": "Вторник"},
        {"name": "Среда"},
        {"name": "Четверг"},
        {"name": "Пятница"},
        {"name": "Суббота"},
        {"name": "Воскресение"},

    ]

    _initial_classes_type = [
        {"name": "Рисование"},
        {"name": "Акробатика"},
        {"name": "Танцы"}
    ]

    _initial_teachers = [
        {"name": "Ивано Иван Иванович"}
    ]


    dataver_path = get_appdata("data_version")
    if not os.path.exists(dataver_path):
        f = open(dataver_path, "w")
        f.write("0")
        f.close()

    f = open(dataver_path, "r")
    dataver = int(f.read())
    f.close()

    if dataver < 1:
        for x in _initial_event_types:
            conn.execute(insert(event_types_table).values(x))
        for x in _initial_events:
            conn.execute(insert(events_table).values(x))
    if dataver < 2:
        for x in _initial_rooms:
            conn.execute(insert(rooms_table).values(x))
        for x in _initial_labor_types:
            conn.execute(insert(labor_types_table).values(x))
        for x in _initial_labor_requests:
            conn.execute(insert(labor_requests_table).values(x))

    if dataver<3:
        for x in _initial_booking:
            conn.execute(insert(booking_table).values(x))
    if dataver < 4:
        for x in _initial_week_days:
            conn.execute(insert(week_days_table).values(x))
        for x in _initial_classes_type:
            conn.execute(insert(classes_type_table).values(x))
        for x in _initial_teachers:
            conn.execute(insert(teachers_table).values(x))


    f = open(dataver_path, "w")
    f.write("4")  # максимальная версия, менять с каждым дефолтным заполнением
    f.close()

    conn.commit()
