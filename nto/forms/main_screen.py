from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QWidget

from nto.forms.compiled.main import Ui_Main

if TYPE_CHECKING:
    from nto.core.main_window import AppWindow


class MainScreen(QWidget, Ui_Main):
    def __init__(self, window: AppWindow) -> None:
        QWidget.__init__(self)
        self.setupUi(self)

        self.main_window = window

        self.OpenEducation.clicked.connect(self.handle_open_education)
        self.OpenEntertainment.clicked.connect(self.handle_open_entertainment)
        self.OpenEnlightenment.clicked.connect(self.handle_open_enlightenment)
        self.OpenLaborRequestsDesktop.clicked.connect(
            self.handle_open_labor_requests_desktop
        )

    def handle_open_education(self) -> None:
        self.main_window.push_screen("EducationDashboard")

    def handle_open_enlightenment(self) -> None:
        self.main_window.push_screen("EnlightenmentDashboard")

    def handle_open_entertainment(self) -> None:
        self.main_window.push_screen("EntertainmentDashboard")

    def handle_open_labor_requests_desktop(self) -> None:
        self.main_window.push_screen(
            "LaborTableViewScreen", read_only=True, desktop=True
        )
