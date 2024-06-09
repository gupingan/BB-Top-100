import sys

from app.interface import logger, common
from app.pyside6.main_window import MainWindow, QtWidgets


def run_app():
    logger.register_logger(common.app_logs_path, common.is_debug)
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
