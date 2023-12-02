from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QWidget

from nto.forms.compiled.enlightenment_dashboard import \
    Ui_EnlightenmentDashboard
from nto.forms.primitives import (RecordEditorPrimitiveDate,
                                  RecordEditorPrimitiveMultilineText,
                                  RecordEditorPrimitiveRelation,
                                  RecordEditorPrimitiveText, RecordEditorPrimitiveDateTime)
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

