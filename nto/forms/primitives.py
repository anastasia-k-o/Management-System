from datetime import date, datetime
from typing import Any, Dict

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (QComboBox, QDateEdit, QDialog, QHBoxLayout,
                             QLineEdit, QMessageBox, QPushButton, QSizePolicy,
                             QTextEdit, QVBoxLayout, QWidget, QDateTimeEdit)

from nto.forms.compiled.relation_table_chooser import Ui_RelationTableView


class RecordEditorPrimitive(QWidget):
    schema: Dict
    title: str

    def __init__(self):
        super().__init__()

    def set_schema(self, schema={}):
        self.schema = schema

    def set_title(self, title=""):
        self.title = title

    def validate(self) -> bool:
        return True

    def get_value(self) -> Any:
        pass

    def show_error(self, text: str) -> None:
        msg = QMessageBox(self)
        msg.setText(text)

        msg.exec_()

        msg.deleteLater()


class RecordEditorPrimitiveEnum(RecordEditorPrimitive):
    def __init__(self, name="", initial_data=0) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        self.name = name

        self.combo = QComboBox()
        self.initial_data = 0 if not initial_data else initial_data

        layout.addWidget(self.combo)

        layout.setContentsMargins(0, 0, 0, 0)

    def set_schema(self, schema={}):
        self.schema = schema

        self.combo.setEnabled(not self.schema.get("read_only", False))
        self.combo.setStyleSheet("color: palette(text)")

        self.fill()
        self.combo.setCurrentIndex(self.initial_data)

    def fill(self) -> None:
        for x in self.schema["variants"]:
            self.combo.addItem(x)

    def validate(self) -> bool:
        return True

    def get_value(self) -> Any:
        return self.combo.currentIndex()


class RecordEditorPrimitiveText(RecordEditorPrimitive):
    def __init__(self, name="", initial_data="") -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        self.name = name

        self.line = QLineEdit()
        self.line.setText(initial_data)

        layout.addWidget(self.line)

        layout.setContentsMargins(0, 0, 0, 0)

    def validate(self) -> bool:
        if (
            not self.schema.get("can_be_empty", False)
            and self.line.text().strip() == ""
        ):
            self.show_error(f'Поле "{self.title}" не может быть пустым')

            return False

        return True

    def get_value(self) -> str:
        return self.line.text().strip()


class RecordEditorPrimitiveMultilineText(RecordEditorPrimitive):
    def __init__(self, name="", initial_data="") -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        self.name = name
        self.line = QTextEdit()
        self.line.setText(initial_data)

        layout.addWidget(self.line)

        layout.setContentsMargins(0, 0, 0, 0)

    def set_schema(self, schema={}):
        self.schema = schema

        self.line.setReadOnly(self.schema.get("read_only", False))

    def validate(self) -> bool:
        if (
            not self.schema.get("can_be_empty", True)
            and self.line.toPlainText().strip() == ""
        ):
            self.show_error(f'Поле "{self.title}" не может быть пустым')

            return False

        return True

    def get_value(self) -> str:
        return self.line.toPlainText().strip()


class RecordEditorPrimitiveDate(RecordEditorPrimitive):
    def __init__(self, name="", initial_data=date) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        self.name = name
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        if not initial_data:
            initial_data = date.today()

        self.date.setDate(
            QDate(
                initial_data.year,  # type: ignore
                initial_data.month,  # type: ignore
                initial_data.day,  # type: ignore
            )
        )

        layout.addWidget(self.date)

        layout.setContentsMargins(0, 0, 0, 0)

    def set_schema(self, schema={}) -> None:
        super().set_schema(schema)

        self.date.setReadOnly(self.schema.get("read_only", False))

    def get_value(self) -> date:
        d = self.date.date()

        return date(d.year(), d.month(), d.day())


class RecordEditorPrimitiveRelationChooser(QWidget, Ui_RelationTableView):
    dialog: QDialog

    def __init__(self, read=lambda: None, name_title="Название") -> None:
        QWidget.__init__(self)
        self.setupUi(self)

        self.read = read
        self.name_title = name_title

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([self.name_title])

        self.Table.setModel(self.model)

        self.ChooseButton.clicked.connect(self.handle_choose)
        self.Table.doubleClicked.connect(self.handle_choose)

        self.selected_id = 0

        self.fill_data()

    def set_dialog(self, diag):
        self.dialog = diag

    def fill_data(self) -> None:
        data = self.read()
        self.model.clear()

        for x in data:
            name = QStandardItem(x["name"])
            name.setData(x["id"])

            self.model.appendRow(name)

        self.model.setHorizontalHeaderLabels([self.name_title])

    def handle_choose(self) -> None:
        selected_indexes = self.Table.selectionModel().selectedIndexes()
        if len(selected_indexes) == 0:
            return

        self.selected_id = self.model.item(
            selected_indexes[0].row(), selected_indexes[0].column()
        ).data()  # type: ignore

        self.dialog.close()

    def get_value(self) -> int:
        return self.selected_id


class RecordEditorPrimitiveRelation(RecordEditorPrimitive):
    def __init__(self, name="", initial_data=0) -> None:
        super().__init__()

        layout = QHBoxLayout(self)

        self.name = name

        self.button = QPushButton("Выбрать")
        self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.line = QLineEdit()

        self.line.setReadOnly(True)

        layout.addWidget(self.line)
        layout.addWidget(self.button)

        self.data = initial_data

        self.button.clicked.connect(self.handle_press)

        layout.setContentsMargins(0, 0, 0, 0)

    def set_schema(self, schema={}):
        self.schema = schema

        initial_name = schema["read_one"](self.data)
        self.line.setText(initial_name["name"] if initial_name else "")

        if self.schema.get("read_only", False):
            self.button.hide()

    def handle_press(self) -> None:
        diag = QDialog(self)

        chooser = RecordEditorPrimitiveRelationChooser(
            read=self.schema["read"],
            name_title=self.schema.get("name_title", "Название"),
        )

        box = QVBoxLayout(diag)
        box.addWidget(chooser)

        diag.resize(400, 320)
        diag.setLayout(box)

        chooser.set_dialog(diag)

        diag.exec_()

        data = chooser.get_value()

        diag.deleteLater()
        chooser.deleteLater()
        box.deleteLater()

        if data == 0:
            return

        self.data = data
        self.line.setText(self.schema["read_one"](self.data)["name"])

    def validate(self) -> bool:
        if not self.schema.get("can_be_empty", False) and not self.data:
            self.show_error(f'Поле "{self.title}" не может быть пустым')

            return False

        return True

    def get_value(self) -> int:
        return self.data



class RecordEditorPrimitiveDateTime(RecordEditorPrimitive):
    def __init__(self, name="", initial_data=datetime) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        self.name = name
        self.date = QDateTimeEdit()
        self.date.setCalendarPopup(True)
        if not initial_data:
            initial_data = datetime.today()

        self.date.setDateTime(
                initial_data
        )

        layout.addWidget(self.date)

        layout.setContentsMargins(0, 0, 0, 0)

    def set_schema(self, schema={}) -> None:
        super().set_schema(schema)

        self.date.setReadOnly(self.schema.get("read_only", False))

    def get_value(self) -> date:
        d = self.date.date()
        t = self.date.time()

        return datetime(d.year(), d.month(), d.day(), t.hour(), t.minute(), t.second())

