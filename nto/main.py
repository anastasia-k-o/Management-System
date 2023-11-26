from PyQt5.QtWidgets import QApplication
from nto.core.database import fill_initial_data

from nto.core.main_window import AppWindow

import qdarktheme
import sys


if __name__ == "__main__":
    fill_initial_data()

    qdarktheme.enable_hi_dpi()

    app = QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    
    main_window = AppWindow()
    main_window.show()

    app.exec_()

    sys.exit(0)
