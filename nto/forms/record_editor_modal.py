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
            booking=None,
            read=lambda: None,
            title=None
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

        if self.read_only:
            self.SaveButton.hide()

        if booking is None:
            self.bookButton.hide()
        else:
            self.booking_view = booking
            self.bookButton.clicked.connect(self.handle_open_book)

    def render(self, initial_data={}) -> None:
        combo_week_days = None
        for x in self.schema:
            prim: RecordEditorPrimitive = x["primitive"](
                name=x["name"], initial_data=initial_data.get(x["name"], "")
            )
            if 'class_day' in x['name'] and combo_week_days is not None:
                combo_week_days.days.append(prim)
            if x['name'] == 'class_time':
                combo_week_days = prim
                combo_week_days.form = self.Form

            if x.get("read_only", "undef") == "undef":
                x["read_only"] = self.read_only

            prim.set_schema(x)
            prim.set_title(x["label"])


            self.Form.addRow(x["label"], prim)

        if combo_week_days is not None:
            combo_week_days.check()

    def handle_save(self):
        newdata = {}

        for i in range(self.Form.rowCount() * 2):
            w = self.Form.itemAt(i).widget()

            if isinstance(w, QLabel):
                continue

            if not w.validate():
                return

            if not w.get_value():
                newdata[w.name] = None
            else:
                newdata[w.name] = w.get_value()
        if self.title == 'Бронирование помещений':
            all_bookings = self.read()
            possible_place = self.schema[1]['read_one'](newdata['room_id'])['events_number'] + 1
            available_place = possible_place
            for booking in all_bookings:
                if booking['room_id'] == newdata['room_id'] and booking['date_start'] <= newdata['date_end'] and \
                        newdata['date_start'] <= booking['date_end'] and self.row_id != booking['id']:
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
        elif self.title == "Работа кружков":
            newdata_days = {newdata['class_day1']}
            if newdata['class_day2'] is not None:
                newdata_days.add(newdata['class_day2'])
            if  newdata['class_day3'] is not None:
                newdata_days.add(newdata['class_day3'])
            all_circles = self.read()
            flag = 0
            for circle in all_circles:
                circle_days = {circle['class_day1']}
                if circle['class_day2'] is not None:
                    circle_days.add(circle['class_day2'])
                if circle['class_day3'] is not None:
                    circle_days.add(circle['class_day3'])
                if (circle['auditorium_id'] == newdata['auditorium_id'] or circle['teacher_id'] == newdata['teacher_id']) and \
                        circle['class_start'] <= newdata['class_end'] and \
                        circle_days.intersection(newdata_days) and self.row_id != circle['id']:
                    flag += 1
            if flag > 0:
                msg = QMessageBox()
                msg.setText("Невозможно сохранить, запись пересекается в другим кружком ")
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
        self.booking_view.handle_add_item(data={'event_id': self.row_id})
