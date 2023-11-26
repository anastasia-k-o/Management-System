from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QWidget

from nto.forms.compiled.education_dashboard import Ui_EducationDashboard
from nto.forms.primitives import RecordEditorPrimitiveText
from nto.forms.table_view_screen import (TableViewGenericCreatorAndUpdater,
                                         TableViewGenericDeleter,
                                         TableViewGenericOneReader,
                                         TableViewGenericReader)
from nto.models import tables

if TYPE_CHECKING:
    from nto.core.main_window import AppWindow


class EducationDashboard(QWidget, Ui_EducationDashboard):
    def __init__(self, window: AppWindow) -> None:
        QWidget.__init__(self)
        self.setupUi(self)

        self.main_window = window

        self.BackButton.clicked.connect(self.main_window.pop_screen)

        self.OpenRooms.clicked.connect(self.handle_open_rooms)

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
