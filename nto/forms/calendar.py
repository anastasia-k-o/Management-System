from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QHBoxLayout, QPushButton, QLabel
from PyQt5.QtWidgets import QWidget

if TYPE_CHECKING:
    from nto.core.main_window import AppWindow
# from sqlalchemy import select, and_

from nto.core.database import conn
from nto.models.tables import (booking_table)

from nto.forms.compiled.calendar_table import \
    Ui_CalendarWindow


class CalendarViewScreen(QWidget, Ui_CalendarWindow):
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
            booking=None
    ) -> None:
        QWidget.__init__(self)
        self.setupUi(self)
        self.bookingHistoryTitle.setText(title)
        self.title = title
        self.main_window = window
        self.schema = schema
        self.name_title = name_title

        self.create_update = create_update
        self.read = read
        self.read_one = read_one
        self.delete = delete

        self.booking = booking

        self.post_fill_data = post_fill_data


        self.BackButton.clicked.connect(self.main_window.pop_screen)
        self.buttonPreviousWeek.clicked.connect(self.prevWeek)
        self.buttonNextWeek.clicked.connect(self.nextWeek)

        self.layout().addWidget(QWidget() if not tooltip else tooltip)  # type: ignore
        self.currentMonday = datetime.now().date() - timedelta(days=datetime.now().weekday())


        self.fill_data()

    def fill_data(self) -> None:

        self.setupRowHeaders()
        self.updateTableHeaders()
        self.updateDateLabel()

        self.setupEvents()

        self.post_fill_data(self)

    def fetch_events_for_week(self, start_date):
        end_date = start_date + timedelta(days=7)
        events = self.read()

        calendar_events = []
        for event in events:
            event_day = event.date_start
            if start_date <= event_day < end_date:
                days = {event.class_day1}
                if event.class_day2 is not None:
                    days.add(event.class_day2)
                if event.class_day2 is not None:
                    days.add(event.class_day3)
                start_datetime = datetime.combine(datetime.today(), event.class_start),
                end_datetime = datetime.combine(datetime.today(), event.class_end),
                duration_timedelta = end_datetime - start_datetime,
                duration_hours = duration_timedelta.seconds // 3600
                for day in days:
                    calendar_events.append({
                        "name": event.name,
                        "day": day,  # 0 - начало недели, 6 - конец недели
                        "start_hour": event.class_start.hour,
                        "duration": duration_hours

                    })
        return calendar_events

    def setupEvents(self):
        self.clearEvents()

        events = self.fetch_events_for_week(self.currentMonday)
        for event in events:
            for hour in range(event["start_hour"], event["start_hour"] + event["duration"]):
                eventItem = QTableWidgetItem(event["name"])
                # Настройка внешнего вида ячейки в зависимости от типа мероприятия
                eventItem.setBackground(Qt.yellow if event["room_id"] != 0 else Qt.green)
                self.tableTime.setItem(hour, event["day"], eventItem)
    #
    def clearEvents(self):
        for row in range(self.tableTime.rowCount()):
            for col in range(self.tableTime.columnCount()):
                self.tableTime.setItem(row, col, QTableWidgetItem(""))

    def updateDateLabel(self):
        endDate = self.currentMonday + timedelta(days=6)
        self.labelDateRange.setText(f'{self.currentMonday.strftime("%d.%m.%Y")} - {endDate.strftime("%d.%m.%Y")}')

    def setupRowHeaders(self):
        self.tableTime.setVerticalHeaderLabels([f'{hour}:00' for hour in range(24)])

    def updateTableHeaders(self):
        for i in range(7):
            date = self.currentMonday + timedelta(days=i)
            self.tableTime.setHorizontalHeaderItem(i, QTableWidgetItem(date.strftime('%d.%m - %A')))
    #
    def prevWeek(self):
        self.currentMonday -= timedelta(days=7)
        self.updateDateLabel()
        self.updateTableHeaders()
        self.setupEvents()

    def nextWeek(self):
        self.currentMonday += timedelta(days=7)
        self.updateDateLabel()
        self.updateTableHeaders()
        self.setupEvents()
