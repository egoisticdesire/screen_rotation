import sys

from PyQt6 import QtWidgets

from widgets.system_tray_icon import SystemTrayIcon


def main():
    app = QtWidgets.QApplication(sys.argv)

    tray_icon = SystemTrayIcon()
    tray_icon.show()

    try:
        app.exec()
    except Exception as e:
        print(f'[ERROR] {e}')


if __name__ == '__main__':
    main()
