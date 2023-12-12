from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QHBoxLayout, QPushButton, QLabel
from PyQt5.QtWidgets import QWidget

if TYPE_CHECKING:
    from nto.core.main_window import AppWindow
from sqlalchemy import select, and_

from nto.core.database import conn
from nto.models.tables import (booking_table)

from nto.forms.compiled.calendar import \
    Ui_CalendarApp


class CalendarApp(QWidget, Ui_CalendarApp):
    def __init__(self, window: AppWindow) -> None:
        QWidget.__init__(self)
        self.setupUi(self)
        self.main_window = window

        self.setWindowTitle('Календарь Мероприятий')
        self.setGeometry(100, 100, 800, 600)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(24)
        self.tableWidget.setColumnCount(7)

        self.currentMonday = datetime.now().date() - timedelta(days=datetime.now().weekday())

        self.labelDateRange = QLabel(self)
        self.buttonPreviousWeek = QPushButton('<', self)
        self.buttonNextWeek = QPushButton('>', self)

        self.buttonPreviousWeek.clicked.connect(self.prevWeek())
        self.buttonNextWeek.clicked.connect(self.nextWeek())

        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.buttonPreviousWeek)
        controlLayout.addWidget(self.labelDateRange)
        controlLayout.addWidget(self.buttonNextWeek)

        layout = QVBoxLayout()
        layout.addLayout(controlLayout)
        layout.addWidget(self.tableWidget)

        container = QWidget()
        container.setLayout(layout)

        self.updateDateLabel()
        self.updateTableHeaders()
        self.setupRowHeaders()

    def fetch_events_for_week(session, start_date):
        end_date = start_date + timedelta(days=7)
        events = conn.execute(select(booking_table).where(and_(booking_table.c.date_start >= start_date, booking_table.c.date_start < end_date)))

        calendar_events = []
        for event in events:
            event_day = event.date_start.date()
            if start_date <= event_day < end_date:
                calendar_events.append({
                    "name": event.description,
                    "day": (event_day - start_date).days,  # 0 - начало недели, 6 - конец недели
                    "start_hour": event.date_start.hour,
                    "duration": (event.date_end - event.date_start).seconds // 3600
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
                self.tableWidget.setItem(hour, event["day"], eventItem)

    def clearEvents(self):
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(row, col, QTableWidgetItem(""))

    def updateDateLabel(self):
        endDate = self.currentMonday + timedelta(days=6)
        self.labelDateRange.setText(f'{self.currentMonday.strftime("%d.%m.%Y")} - {endDate.strftime("%d.%m.%Y")}')

    def setupRowHeaders(self):
        self.tableWidget.setVerticalHeaderLabels([f'{hour}:00' for hour in range(24)])

    def updateTableHeaders(self):
        for i in range(7):
            date = self.currentMonday + timedelta(days=i)
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(date.strftime('%d.%m - %A')))

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
