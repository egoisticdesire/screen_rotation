import sys

from PyQt6 import QtWidgets

from utils.logger import Logger
from widgets.system_tray_icon import SystemTrayIcon

LOGGER = Logger(name=__name__)


def main():
    app = QtWidgets.QApplication(sys.argv)

    tray_icon = SystemTrayIcon()
    tray_icon.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as e:
        LOGGER.log_critical(f'An error occurred while running the application: {e}')
    except Exception as e:
        LOGGER.log_error(f'An error occurred while running the application: {e}')
