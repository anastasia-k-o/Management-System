from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QIcon, QPixmap, QStandardItem
from PyQt5.QtWidgets import QMessageBox, QPushButton, QSizePolicy
from sqlalchemy import select, update

from nto.core.database import conn
from nto.forms.labor_requests_tooltip import LaborRequestsTooltip
from nto.forms.primitives import (RecordEditorPrimitiveDate,
                                  RecordEditorPrimitiveEnum,
                                  RecordEditorPrimitiveMultilineText,
                                  RecordEditorPrimitiveRelation,
                                  RecordEditorPrimitiveText)
from nto.forms.table_view_screen import (TableViewGenericCreatorAndUpdater,
                                         TableViewGenericDeleter,
                                         TableViewGenericOneReader,
                                         TableViewGenericReader,
                                         TableViewScreen)
from nto.models import tables


class LaborTableViewScreen(TableViewScreen):
    def __init__(self, window, desktop=False, read_only=False) -> None:
        labor_tooltip = LaborRequestsTooltip()
        labor_tooltip.TypeSelector.addItem("Все", 0)

        self.selected_type = 0
        self.desktop = desktop

        for x in conn.execute(select(tables.labor_types_table)).all():
            labor_tooltip.TypeSelector.addItem(x.name, x.id)

        labor_tooltip.TypeSelector.currentIndexChanged.connect(
            self.type_selector_index_changed
        )

        if desktop:
            labor_tooltip.hide_colors_description()

        kwargs = {}

        kwargs["read_only"] = read_only
        kwargs["window"] = window
        kwargs["title"] = "Заявки на выполнение работ"
        kwargs["name_title"] = "Заголовок"
        kwargs["read"] = TableViewGenericReader(tables.labor_requests_table).do
        kwargs["read_one"] = TableViewGenericOneReader(tables.labor_requests_table).do
        kwargs["create_update"] = TableViewGenericCreatorAndUpdater(
            tables.labor_requests_table
        ).do
        kwargs["delete"] = TableViewGenericDeleter(tables.labor_requests_table).do
        kwargs["tooltip"] = labor_tooltip
        kwargs["schema"] = [
            {
                "name": "name",
                "label": "Заголовок",
                "primitive": RecordEditorPrimitiveText,
            },
            {
                "name": "labor_type_id",
                "label": "Тип работы",
                "primitive": RecordEditorPrimitiveRelation,
                "read": TableViewGenericReader(tables.labor_types_table).do,
                "read_one": TableViewGenericOneReader(tables.labor_types_table).do,
            },
            {
                "name": "room_id",
                "label": "Помещение",
                "primitive": RecordEditorPrimitiveRelation,
                "read": TableViewGenericReader(tables.rooms_table).do,
                "read_one": TableViewGenericOneReader(tables.rooms_table).do,
            },
            {
                "name": "event_id",
                "label": "Мероприятие",
                "primitive": RecordEditorPrimitiveRelation,
                "read": TableViewGenericReader(tables.events_table).do,
                "read_one": TableViewGenericOneReader(tables.events_table).do,
            },
            {
                "name": "deadline_date",
                "label": "Срок выполнения",
                "primitive": RecordEditorPrimitiveDate,
            },
            {
                "name": "status",
                "label": "Статус",
                "primitive": RecordEditorPrimitiveEnum,
                "variants": ["Создана", "К выполнению", "Выполнена"],
            },
            {
                "name": "description",
                "label": "Описание",
                "primitive": RecordEditorPrimitiveMultilineText,
            },
            {
                "name": "registration_date",
                "label": "Дата регистрации",
                "primitive": RecordEditorPrimitiveDate,
                "read_only": True,
            },
        ]

        super().__init__(**kwargs)

        done_button_icon = QIcon()
        done_button_icon.addPixmap(QPixmap(":/checkmark/checkmark.svg"))

        self.done_button = QPushButton()
        self.done_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.done_button.setIcon(done_button_icon)
        self.done_button.setIconSize(QSize(24, 24))
        self.done_button.setFlat(True)

        self.done_button.clicked.connect(self.handle_done_button)

        if self.desktop:
            self.ButtonsHeader.addWidget(self.done_button)

    def type_selector_index_changed(self, index: int) -> None:
        self.selected_type = index

        self.fill_data()

    def fill_data(self) -> None:
        pre_data = self.read()
        data = []

        for x in pre_data:
            if self.desktop and (not (x["status"] == 1)):
                continue

            if x["labor_type_id"] == self.selected_type or self.selected_type == 0:
                data.append(x)

        self.model.clear()

        self.model.setHorizontalHeaderLabels(
            ["Срок выполнения", "Заголовок"] if self.desktop else ["Заголовок"]
        )

        for x in data:
            cols = []

            name = QStandardItem(str(x["name"]))
            name.setData(x["id"])

            if not self.desktop:
                if x["status"] == 0:
                    name.setBackground(QColor("white"))
                elif x["status"] == 1:
                    name.setBackground(QColor("pink"))
                elif x["status"] == 2:
                    name.setBackground(QColor("gray"))
                    name.setData(QColor("white"), Qt.ForegroundRole)  # type: ignore

            if self.desktop:
                dat = QStandardItem(x["deadline_date"].strftime("%d.%m.%Y"))
                dat.setData(x["id"])

                cols.append(dat)

            cols.append(name)

            self.model.appendRow(cols)

        self.post_fill_data(self)

    def handle_done_button(self) -> None:
        ids = list(set(self.get_selected_indexes()))

        for x in ids:
            conn.execute(
                update(tables.labor_requests_table)
                .where(tables.labor_requests_table.c.id == x)
                .values({"status": 2})
            )

            conn.commit()

            msg = QMessageBox()
            msg.setWindowTitle("Успешно")
            msg.setText("Заявка успешно помечена как выполненная")

            msg.exec_()
            msg.deleteLater()

        self.fill_data()
