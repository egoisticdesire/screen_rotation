import socket
import sys

from PyQt6 import QtGui, QtWidgets

from utils import variables as var
from utils.logger import Logger
from widgets.system_tray_icon import SystemTrayIcon

LOGGER = Logger(name=__name__)


def main():
    app = QtWidgets.QApplication(sys.argv)

    tray_icon = SystemTrayIcon()
    tray_icon.show()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((var.LOCALHOST, var.PORT))
            sys.exit(app.exec())
    except socket.error:
        tray_icon.showMessage(None, var.APP_ALREADY_RUNNING_MESSAGE, QtGui.QIcon(var.ICONS['_screen_rotation']))
        print(var.ICONS['_screen_rotation'])
        LOGGER.log_error(f'Port {var.PORT} is already in use')


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as e:
        LOGGER.log_critical(f'An error occurred while running the application: {e}')
    except Exception as e:
        LOGGER.log_error(f'An error occurred while running the application: {e}')
