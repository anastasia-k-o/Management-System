from typing import List

from PyQt5.QtWidgets import QMainWindow, QWidget

from nto.forms.education_dashboard import EducationDashboard
from nto.forms.enlightenment_dashboard import EnlightenmentDashboard
from nto.forms.entertainment_dashboard import EntertainmentDashboard
from nto.forms.labor_table_view import LaborTableViewScreen
from nto.forms.main_screen import MainScreen
from nto.forms.table_view_screen import TableViewScreen
from nto.forms.calendar import CalendarViewScreen

screens = {
    "TableViewScreen": TableViewScreen,
    "MainScreen": MainScreen,
    "EnlightenmentDashboard": EnlightenmentDashboard,
    "EducationDashboard": EducationDashboard,
    "EntertainmentDashboard": EntertainmentDashboard,
    "LaborTableViewScreen": LaborTableViewScreen,
    "CalendarViewScreen": CalendarViewScreen,
}


class AppWindow(QMainWindow):
    stack: List[QWidget] = []

    def __init__(self) -> None:
        super().__init__()

        self.setMinimumSize(640, 480)
        self.setWindowTitle("Культурный центр ЗИЛ")

        self.switch_screen("LaborTableViewScreen", read_only=True, desktop=True)

        self.switch_screen("MainScreen")

    def switch_screen(self, name: str, **kwargs) -> None:
        kwargs["window"] = self

        instance = screens[name](**kwargs)

        for x in self.stack:
            x.deleteLater()

        self.stack.clear()
        self.stack.append(instance)

        self.setCentralWidget(self.stack[-1])
    def give_screen_instance(self, name: str, **kwargs):
        kwargs["window"] = self
        instance = screens[name](**kwargs)
        return instance
    def push_screen(self, name: str, **kwargs) -> None:
        kwargs["window"] = self

        instance = screens[name](**kwargs)
        self.stack[-1].setParent(None)

        self.stack.append(instance)

        self.setCentralWidget(self.stack[-1])

    def pop_screen(self) -> None:
        self.stack.pop().deleteLater()

        self.setCentralWidget(self.stack[-1])
