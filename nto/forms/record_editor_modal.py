from PyQt5.QtWidgets import QLabel, QMessageBox, QWidget, QDialog, QVBoxLayout

from nto.forms.compiled.designed_record_editor import Ui_RecordEditor
from nto.forms.primitives import RecordEditorPrimitive

class RecordEditorModal(QWidget, Ui_RecordEditor):
    def __init__(
        self,
        schema={},
        initial_data={},
        create_update=lambda: None,
        after_hook=lambda: None,
        read_only=False,
        booking = None,
        read = lambda: None,
        title = None
    ) -> None:
        QWidget.__init__(self)
        self.setupUi(self)

        self.row_id = initial_data.get("id", None)
        self.schema = schema
        self.create_update = create_update
        self.after_hook = after_hook
        self.read = read
        self.title = title

        self.read_only = read_only

        self.render(initial_data)
        self.booking = booking

        self.SaveButton.clicked.connect(self.handle_save)

        if booking is None:
            self.bookButton.hide()
        else:
            self.booking_view = booking
            self.bookButton.clicked.connect(self.handle_open_book)

    def render(self, initial_data={}) -> None:
        for x in self.schema:
            prim: RecordEditorPrimitive = x["primitive"](
                name=x["name"], initial_data=initial_data.get(x["name"], "")
            )

            if x.get("read_only", "undef") == "undef":
                x["read_only"] = self.read_only

            prim.set_schema(x)
            prim.set_title(x["label"])

            self.Form.addRow(x["label"], prim)

    def handle_save(self):
        newdata = {}

        for i in range(self.Form.rowCount() * 2):
            w = self.Form.itemAt(i).widget()

            if isinstance(w, QLabel):
                continue

            if not w.validate():
                return

            newdata[w.name] = w.get_value()
        if self.title == 'Бронирование помещений':
            self.row_id = None
            all_bookings = self.read()
            possible_place = self.schema[1]['read_one'](newdata['room_id'])['events_number'] + 1
            available_place =possible_place
            for booking in all_bookings:
                if booking['room_id'] == newdata['room_id'] and booking['date_start'] <= newdata['date_end'] and newdata['date_start'] <= booking['date_end'] :
                    available_place -= booking['booking_part'] + 1
            if available_place <= 0:
                msg = QMessageBox()
                msg.setText("Бронирование недоступно, помещение занято")

            elif available_place == 1 and newdata['booking_part'] == 1 and possible_place != 1:
                msg = QMessageBox()
                msg.setText("Невозможно заброинровать помещение полностью, доступна только часть")
            else:
                msg = QMessageBox()
                msg.setText("Запись успешно " + ("изменена" if self.row_id else "создана"))

                self.row_id = self.create_update(self.row_id, newdata)
        else:
            msg = QMessageBox()
            msg.setText("Запись успешно " + ("изменена" if self.row_id else "создана"))

            self.row_id = self.create_update(self.row_id, newdata)

        self.after_hook()

        msg.exec_()

    def handle_open_book(self):
        self.booking_view.handle_add_item(data = {'event_id' : self.row_id})

