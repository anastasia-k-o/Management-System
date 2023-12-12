from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Dict, List

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (QDialog, QMessageBox, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)
from sqlalchemy import Row, RowMapping, Table, delete, insert, select, update
from sqlalchemy.inspection import exc

from nto.core.database import conn
from nto.forms.compiled.designed_table_view import Ui_TableView
from nto.forms.primitives import RecordEditorPrimitiveEnum
from nto.forms.record_editor_modal import RecordEditorModal

if TYPE_CHECKING:
    from nto.core.main_window import AppWindow


class TableViewGenericReader:
    def __init__(self, table: Table) -> None:
        self.table = table

    def do(self) -> Sequence[RowMapping]:
        return conn.execute(select(self.table)).mappings().all()


class TableViewGenericCreatorAndUpdater:
    def __init__(self, table: Table) -> None:
        self.table = table

    def do(self, id: int, data: Dict) -> int:
        if id:
            conn.execute(
                update(self.table).where(self.table.c.id == id).values(data),
            )

            conn.commit()
        else:
            res = conn.execute(insert(self.table).values(data))

            conn.commit()

            id = res.lastrowid

        return id


class TableViewGenericOneReader:
    def __init__(self, table: Table) -> None:
        self.table = table

    def do(self, id: int) -> Row:
        return (
            conn.execute(select(self.table).where(self.table.c.id == id))
            .mappings()
            .first()
        )  # type: ignore


class TableViewGenericDeleter:
    def __init__(self, table: Table) -> None:
        self.table = table

    def do(self, id: int) -> None:
        conn.execute(delete(self.table).where(self.table.c.id == id))

        conn.commit()


class TableViewScreen(QWidget, Ui_TableView):
    def __init__(
        self,
        window: AppWindow,
        schema={},
        title="Таблица",
        name_title="Название",
        create_update=lambda: None,
        read=lambda: [],
        delete=lambda: None,
        read_one=lambda: None,
        post_fill_data=lambda _: None,
        tooltip=None,
        read_only=False,
        booking = None
    ) -> None:
        QWidget.__init__(self)
        self.setupUi(self)

        self.ViewNameText.setText(title)
        self.title = title
        self.main_window = window
        self.schema = schema
        self.name_title = name_title

        self.create_update = create_update
        self.read = read
        self.read_one = read_one
        self.delete = delete

        self.read_only = read_only
        self.booking = booking

        self.post_fill_data = post_fill_data

        self.model = QStandardItemModel()
        self.Table.setModel(self.model)

        self.model.setHorizontalHeaderLabels([self.name_title])

        if not self.read_only:
            self.Table.doubleClicked.connect(self.handle_edit_item)
            self.EditButton.clicked.connect(self.handle_edit_item)
            self.AddButton.clicked.connect(self.handle_add_item)
            self.DeleteButton.clicked.connect(self.handle_delete_item)

        if self.read_only:
            self.EditButton.hide()
            self.AddButton.hide()
            self.DeleteButton.hide()

            view_button_icon = QIcon()
            view_button_icon.addPixmap(QPixmap(":/view/view.svg"))

            self.view_button = QPushButton()
            self.view_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.view_button.setIcon(view_button_icon)
            self.view_button.setIconSize(QSize(24, 24))
            self.view_button.setFlat(True)

            self.Table.doubleClicked.connect(self.handle_view_item)
            self.view_button.clicked.connect(self.handle_view_item)

            self.ButtonsHeader.addWidget(self.view_button)

        self.ExitButton.clicked.connect(self.main_window.pop_screen)

        self.layout().addWidget(QWidget() if not tooltip else tooltip)  # type: ignore

        self.fill_data()

    def fill_data(self) -> None:
        data = self.read()

        self.model.clear()

        for x in data:
            if 'name' not in x and self.title=='Бронирование помещений':
                text_name = f"Бронирование помещения с {x['date_start']} до {x['date_end']}"
            else:
                text_name = str(x["name"])
            name = QStandardItem(text_name)
            name.setData(x["id"])

            self.model.appendRow([name])

        self.model.setHorizontalHeaderLabels([self.name_title])

        self.post_fill_data(self)

    def get_selected_indexes(self) -> List[int]:
        selected_indexes = self.Table.selectionModel().selectedIndexes()
        ids = []

        for x in selected_indexes:
            ids.append(
                self.model.item(x.row(), x.column()).data(),  # type: ignore
            )

        return ids

    def handle_edit_item(self) -> None:
        ids = self.get_selected_indexes()


        for x in ids:
            data = self.read_one(x)

            editor = RecordEditorModal(
                schema=self.schema,
                initial_data=data,
                create_update=self.create_update,
                after_hook=self.fill_data,
                booking = self.booking,
                read = self.read,
                title = self.title

            )


            diag = QDialog(self)
            box = QVBoxLayout(diag)
            box.addWidget(editor)
            diag.setLayout(box)
            diag.setWindowTitle("Редактор записи")
            diag.resize(500, 400)

            diag.exec_()

            self.fill_data()

            editor.deleteLater()
            diag.deleteLater()
            box.deleteLater()

    def handle_add_item(self, data = None) -> None:
        if isinstance(data, dict):
            editor = RecordEditorModal(
                schema=self.schema,
                initial_data=data,
                create_update=self.create_update,
                after_hook=self.fill_data,
                read = self.read,
                title = self.title
            )
        else:
            editor = RecordEditorModal(
                schema=self.schema,
                create_update=self.create_update,
                after_hook=self.fill_data,
                read = self.read,
                title = self.title
            )


        diag = QDialog(self)
        box = QVBoxLayout(diag)
        box.addWidget(editor)
        diag.setLayout(box)
        diag.setWindowTitle("Редактор записи")
        diag.resize(500, 400)

        diag.exec_()

        self.fill_data()

        editor.deleteLater()
        diag.deleteLater()
        box.deleteLater()

    def handle_view_item(self) -> None:
        ids = list(set(self.get_selected_indexes()))

        for x in ids:
            data = self.read_one(x)

            editor = RecordEditorModal(
                schema=self.schema,
                create_update=self.create_update,
                after_hook=self.fill_data,
                read_only=self.read_only,
                booking = self.booking,
                initial_data=data,
                read = self.read,
                title = self.title
            )

            diag = QDialog(self)
            box = QVBoxLayout(diag)
            box.addWidget(editor)
            diag.setLayout(box)
            diag.setWindowTitle("Редактор записи")
            diag.resize(500, 400)

            diag.exec_()

            self.fill_data()

            editor.deleteLater()
            diag.deleteLater()
            box.deleteLater()

    def handle_delete_item(self) -> None:
        ids = self.get_selected_indexes()

        for x in ids:
            try:
                self.delete(x)
            except exc.IntegrityError:
                msg = QMessageBox()

                msg.setText(
                    "Невозможно удалить эту запись, "
                    + "так как от неё зависит другой объект"
                )
                msg.exec_()
                msg.deleteLater()

        self.fill_data()
