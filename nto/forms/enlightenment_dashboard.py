from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QWidget

from nto.forms.compiled.enlightenment_dashboard import \
    Ui_EnlightenmentDashboard
from nto.forms.primitives import (RecordEditorPrimitiveDate,
                                  RecordEditorPrimitiveMultilineText,
                                  RecordEditorPrimitiveRelation,
                                  RecordEditorPrimitiveText, RecordEditorPrimitiveDateTime, RecordEditorPrimitiveEnum,
                                  RecordEditorPrimitiveTime)
from nto.forms.table_view_screen import (TableViewGenericCreatorAndUpdater,
                                         TableViewGenericDeleter,
                                         TableViewGenericOneReader,
                                         TableViewGenericReader)
from nto.models import tables

if TYPE_CHECKING:
    from nto.core.main_window import AppWindow


class EnlightenmentDashboard(QWidget, Ui_EnlightenmentDashboard):
    def __init__(self, window: AppWindow):
        QWidget.__init__(self)
        self.setupUi(self)

        self.main_window = window

        self.BackButton.clicked.connect(self.main_window.pop_screen)

        self.OpenEvents.clicked.connect(self.handle_open_events)
        self.OpenEventTypes.clicked.connect(self.handle_open_event_types)

        self.OpenRooms.clicked.connect(self.handle_open_rooms)
        self.OpenLaborTypes.clicked.connect(self.handle_open_labor_types)
        self.OpenLaborRequests.clicked.connect(self.handle_open_labor_requests)
        self.bookingRooms.clicked.connect(self.handle_open_booking)
        self.classTypes.clicked.connect(self.handle_open_classes_types)
        self.teachers.clicked.connect(self.handle_open_teachers)
        self.weekDays.clicked.connect(self.handle_open_week_days)
        self.workOfClass.clicked.connect(self.handle_open_classes)

    def handle_open_labor_requests(self) -> None:
        self.main_window.push_screen("LaborTableViewScreen")

    def handle_open_labor_types(self) -> None:
        self.main_window.push_screen(
            "TableViewScreen",
            title="Виды работ",
            read=TableViewGenericReader(tables.labor_types_table).do,
            read_one=TableViewGenericOneReader(tables.labor_types_table).do,
            create_update=TableViewGenericCreatorAndUpdater(
                tables.labor_types_table,
            ).do,
            delete=TableViewGenericDeleter(tables.labor_types_table).do,
            schema=[
                {
                    "name": "name",
                    "label": "Название",
                    "primitive": RecordEditorPrimitiveText,
                }
            ],
        )

    def handle_open_rooms(self) -> None:
        self.main_window.push_screen(
            "TableViewScreen",
            title="Помещения",
            read=TableViewGenericReader(tables.rooms_table).do,
            read_one=TableViewGenericOneReader(tables.rooms_table).do,
            create_update=TableViewGenericCreatorAndUpdater(
                tables.rooms_table,
            ).do,
            delete=TableViewGenericDeleter(tables.rooms_table).do,

            schema=[
                {
                    "name": "name",
                    "label": "Название",
                    "primitive": RecordEditorPrimitiveText,
                },
                {
                    "name": "events_number",
                    "label": "Количество мероприятий",
                    "primitive": RecordEditorPrimitiveEnum,
                    "variants": ["Одно мероприятие", "Два мероприятия"]
                }
            ],
        )

    def handle_open_events(self) -> None:
        self.main_window.push_screen(
            "TableViewScreen",
            title="Мероприятия",
            read=TableViewGenericReader(tables.events_table).do,
            read_one=TableViewGenericOneReader(tables.events_table).do,
            create_update=TableViewGenericCreatorAndUpdater(tables.events_table).do,
            delete=TableViewGenericDeleter(tables.events_table).do,
            booking=self.main_window.give_screen_instance(
                "TableViewScreen",
                title="Бронирование помещений",
                read=TableViewGenericReader(tables.booking_table).do,
                read_one=TableViewGenericOneReader(tables.booking_table).do,
                create_update=TableViewGenericCreatorAndUpdater(
                    tables.booking_table,
                ).do,
                delete=TableViewGenericDeleter(tables.booking_table).do,

                schema=[
                    {
                        "name": "date_registration",
                        "label": "Дата создания",
                        "primitive": RecordEditorPrimitiveDate,
                    },
                    {
                        "name": "room_id",
                        "label": "Помещение",
                        "primitive": RecordEditorPrimitiveRelation,
                        "read": TableViewGenericReader(tables.rooms_table).do,
                        "read_one": TableViewGenericOneReader(
                            tables.rooms_table,
                        ).do,
                    },
                    {
                        "name": "event_id",
                        "label": "Мероприятие",
                        "primitive": RecordEditorPrimitiveRelation,
                        "read": TableViewGenericReader(tables.events_table).do,
                        "read_one": TableViewGenericOneReader(
                            tables.events_table,
                        ).do,
                    },
                    {
                        "name": "booking_part",
                        "label": "Мероприятие займет",
                        "primitive": RecordEditorPrimitiveEnum,
                        "variants": ["Часть помещения", "Всё помещение"]
                    },

                    {
                        "name": "date_start",
                        "label": "Дата начала бронирования",
                        "primitive": RecordEditorPrimitiveDateTime,
                    },
                    {
                        "name": "date_end",
                        "label": "Дата конца бронирования",
                        "primitive": RecordEditorPrimitiveDateTime,
                    },
                    {
                        "name": "description",
                        "label": "Описание",
                        "primitive": RecordEditorPrimitiveMultilineText,
                    },
                ],
            ),
            schema=[
                {
                    "name": "name",
                    "label": "Название",
                    "primitive": RecordEditorPrimitiveText,
                },
                {
                    "name": "event_type_id",
                    "label": "Вид",
                    "primitive": RecordEditorPrimitiveRelation,
                    "read": TableViewGenericReader(tables.event_types_table).do,
                    "read_one": TableViewGenericOneReader(
                        tables.event_types_table,
                    ).do,
                },
                {
                    "name": "date",
                    "label": "Дата",
                    "primitive": RecordEditorPrimitiveDate,
                },
                {
                    "name": "description",
                    "label": "Описание",
                    "primitive": RecordEditorPrimitiveMultilineText,
                },
            ],
        )

    def handle_open_event_types(self):
        self.main_window.push_screen(
            "TableViewScreen",
            title="Виды мероприятий",
            read=TableViewGenericReader(tables.event_types_table).do,
            read_one=TableViewGenericOneReader(tables.event_types_table).do,
            create_update=TableViewGenericCreatorAndUpdater(
                tables.event_types_table,
            ).do,
            delete=TableViewGenericDeleter(tables.event_types_table).do,
            schema=[
                {
                    "name": "name",
                    "label": "Название",
                    "primitive": RecordEditorPrimitiveText,
                }
            ],
        )

    def handle_open_booking(self):
        self.main_window.push_screen(
            "TableViewScreen",
            title="Бронирование помещений",
            read=TableViewGenericReader(tables.booking_table).do,
            read_one=TableViewGenericOneReader(tables.booking_table).do,
            create_update=TableViewGenericCreatorAndUpdater(
                tables.booking_table,
            ).do,
            delete=TableViewGenericDeleter(tables.booking_table).do,
            schema=[
                {
                    "name": "date_registration",
                    "label": "Дата создания",
                    "primitive": RecordEditorPrimitiveDate,
                },
                {
                    "name": "room_id",
                    "label": "Помещение",
                    "primitive": RecordEditorPrimitiveRelation,
                    "read": TableViewGenericReader(tables.rooms_table).do,
                    "read_one": TableViewGenericOneReader(
                        tables.rooms_table,
                    ).do,
                },
                {
                    "name": "event_id",
                    "label": "Мероприятие",
                    "primitive": RecordEditorPrimitiveRelation,
                    "read": TableViewGenericReader(tables.events_table).do,
                    "read_one": TableViewGenericOneReader(
                        tables.events_table,
                    ).do,
                },

                {
                    "name": "date_start",
                    "label": "Дата начала бронирования",
                    "primitive": RecordEditorPrimitiveDateTime,
                },
                {
                    "name": "date_end",
                    "label": "Дата конца бронирования",
                    "primitive": RecordEditorPrimitiveDateTime,
                },
                {
                    "name": "description",
                    "label": "Описание",
                    "primitive": RecordEditorPrimitiveMultilineText,
                },
            ],
        )
    def handle_open_classes_types(self):
        self.main_window.push_screen(
            "TableViewScreen",
            title="Виды кружки",
            read=TableViewGenericReader(tables.classes_type_table).do,
            read_one=TableViewGenericOneReader(tables.classes_type_table).do,
            create_update=TableViewGenericCreatorAndUpdater(
                tables.classes_type_table,
            ).do,
            delete=TableViewGenericDeleter(tables.classes_type_table).do,

            schema=[
                {
                    "name": "name",
                    "label": "Название",
                    "primitive": RecordEditorPrimitiveText,
                }
            ],
        )

    def handle_open_teachers(self):
        self.main_window.push_screen(
            "TableViewScreen",
            title="Преподаватели",
            read=TableViewGenericReader(tables.teachers_table).do,
            read_one=TableViewGenericOneReader(tables.teachers_table).do,
            create_update=TableViewGenericCreatorAndUpdater(
                tables.teachers_table,
            ).do,
            delete=TableViewGenericDeleter(tables.teachers_table).do,

            schema=[
                {
                    "name": "name",
                    "label": "Название",
                    "primitive": RecordEditorPrimitiveText,
                }
            ],
        )

    def handle_open_week_days(self):
        self.main_window.push_screen(
            "TableViewScreen",
            title="Дни недели",
            read=TableViewGenericReader(tables.week_days_table).do,
            read_one=TableViewGenericOneReader(tables.week_days_table).do,
            create_update=TableViewGenericCreatorAndUpdater(
                tables.week_days_table,
            ).do,
            delete=TableViewGenericDeleter(tables.week_days_table).do,

            schema=[
                {
                    "name": "name",
                    "label": "Название",
                    "primitive": RecordEditorPrimitiveText,
                }
            ],
        )

    def handle_open_classes(self):
        self.main_window.push_screen(
            "TableViewScreen",
            title="Работа кружков",
            read=TableViewGenericReader(tables.classes_table).do,
            read_one=TableViewGenericOneReader(tables.classes_table).do,
            create_update=TableViewGenericCreatorAndUpdater(
                tables.classes_table,
            ).do,
            delete=TableViewGenericDeleter(tables.classes_table).do,
            schema=[
                {
                    "name": "name",
                    "label": "Название",
                    "primitive": RecordEditorPrimitiveText,
                },
                {
                    "name": "date_start",
                    "label": "Дата начала работы",
                    "primitive": RecordEditorPrimitiveDate,
                },
                {
                    "name": "class_id",
                    "label": "Вид кружка",
                    "primitive": RecordEditorPrimitiveRelation,
                    "read": TableViewGenericReader(tables.classes_type_table).do,
                    "read_one": TableViewGenericOneReader(
                        tables.classes_type_table,
                    ).do,
                },
                {
                    "name": "room_id",
                    "label": "Помещение",
                    "primitive": RecordEditorPrimitiveRelation,
                    "read": TableViewGenericReader(tables.rooms_table).do,
                    "read_one": TableViewGenericOneReader(
                        tables.rooms_table,
                    ).do,
                },

                {
                    "name": "class_time",
                    "label": "Количество занятий в неделю",
                    "primitive": RecordEditorPrimitiveEnum,
                    "variants": ["3","2","1"]
                },
                {
                    "name": "class_day1",
                    "label": "Первый день",
                    "primitive": RecordEditorPrimitiveRelation,
                    "read": TableViewGenericReader(tables.week_days_table).do,
                    "read_one": TableViewGenericOneReader(
                        tables.week_days_table,
                    ).do,
                    "can_be_empty" : True
                },
                {
                    "name": "class_day2",
                    "label": "Второй день",
                    "primitive": RecordEditorPrimitiveRelation,
                    "read": TableViewGenericReader(tables.week_days_table).do,
                    "read_one": TableViewGenericOneReader(
                        tables.week_days_table,
                    ).do,
                    "can_be_empty": True
                },
                {
                    "name": "class_day3",
                    "label": "Третий день",
                    "primitive": RecordEditorPrimitiveRelation,
                    "read": TableViewGenericReader(tables.week_days_table).do,
                    "read_one": TableViewGenericOneReader(
                        tables.week_days_table,
                    ).do,
                    "can_be_empty": True
                },
                {
                    "name": "class_start",
                    "label": "Время начала задания",
                    "primitive": RecordEditorPrimitiveTime,
                },
                {
                    "name": "class_end",
                    "label": "Время конца задания",
                    "primitive": RecordEditorPrimitiveTime,
                },
                {
                    "name": "teacher_id",
                    "label": "Преподаватель",
                    "primitive": RecordEditorPrimitiveRelation,
                    "read": TableViewGenericReader(tables.teachers_table).do,
                    "read_one": TableViewGenericOneReader(
                        tables.teachers_table,
                    ).do,
                },

            ],
        )
