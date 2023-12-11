import sys

from PyQt6 import QtWidgets

from widgets.system_tray_icon import SystemTrayIcon


def main():
    app = QtWidgets.QApplication(sys.argv)

    tray_icon = SystemTrayIcon()
    tray_icon.show()

    app.exec()


if __name__ == '__main__':
    main()
