from PyQt5.QtWidgets import QWidget

from nto.forms.compiled.labor_requests_tooltip import Ui_LaborRequestsTooltip


class LaborRequestsTooltip(QWidget, Ui_LaborRequestsTooltip):
    def __init__(self) -> None:
        QWidget.__init__(self)
        self.setupUi(self)

    def hide_colors_description(self) -> None:
        self.label.hide()
        self.label_2.hide()
        self.label_3.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.hide()
