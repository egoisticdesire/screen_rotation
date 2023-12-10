import sys

import keyboard
import rotatescreen
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from PyQt6.QtGui import QAction, QActionGroup, QIcon


class RoundedCornersQMenu(QMenu):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self._radius = 8
        self.setStyleSheet(
            f'''
                QMenu{{
                    font-size: 16px;
                    background-color: rgb(26, 26, 26);
                    color: rgb(225, 225, 225);
                    border: 1px solid rgb(86, 86, 86);
                    border-radius: {self._radius}px;
                }}
                QMenu::item {{
                    border-radius: 6px;
                    padding: 4px 10px;
                    margin: 4px;
                }}
                QMenu::icon {{
                    padding: 5px 10px;
                }}
                QMenu::item:selected {{
                    background-color: rgb(46, 46, 46);
                }}
                QMenu::item:pressed {{
                    background-color: rgb(36, 36, 36);
                }}
                QMenu::item:disabled {{
                    color: rgb(96, 96, 96);
                }}
                QMenu::item:disabled:selected {{
                    background-color: rgb(36, 36, 36);
                }}
                QMenu::separator {{
                    height: 1px;
                    background-color: rgb(46, 46, 46);
                }}
            '''
        )

    def resizeEvent(self, event):
        path = QtGui.QPainterPath()
        rect = QtCore.QRectF(self.rect()).adjusted(-.5, -.5, -.01, -.01)
        path.addRoundedRect(rect, self._radius, self._radius)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)


class TrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.setToolTip("Screen Rotation")
        self.menu = RoundedCornersQMenu()
        self.menu.setWindowFlags(Qt.WindowType.Popup)
        self.menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.orientation_group = QActionGroup(self)
        self.orientation_group.setExclusive(True)

        self.normal_action = QAction(QIcon('assets/round_screen_lock_landscape_white_48dp.png'), "Normal mode", self)
        self.portrait_action = QAction(QIcon('assets/round_screen_lock_portrait_white_48dp.png'), "Portrait mode", self)
        self.quit_action = QAction(QIcon('assets/round_logout_white_48dp.png'), "Quit", self)

        self.normal_action.setCheckable(True)
        self.portrait_action.setCheckable(True)

        self.normal_action.triggered.connect(lambda: self.__on_orientation_change("landscape"))
        self.portrait_action.triggered.connect(lambda: self.__on_orientation_change("portrait"))
        self.quit_action.triggered.connect(self.__on_exit_callback)

        self.orientation_group.addAction(self.normal_action)
        self.orientation_group.addAction(self.portrait_action)

        self.menu.addAction(self.normal_action)
        self.menu.addAction(self.portrait_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.setContextMenu(self.menu)
        self.__set_keyboard_hotkeys()

        self.__update_actions_state()  # Установка начального состояния активности кнопок

    def __update_actions_state(self):
        screen = rotatescreen.get_primary_display()
        if screen.current_orientation == 0:  # Проверка текущего режима экрана (0 - landscape, 90 - portrait)
            self.normal_action.setChecked(True)
            self.normal_action.setEnabled(False)  # Делаем активной только выбранную опцию
            self.portrait_action.setEnabled(True)
        elif screen.current_orientation == 90:
            self.portrait_action.setChecked(True)
            self.normal_action.setEnabled(True)
            self.portrait_action.setEnabled(False)

    def __on_orientation_change(self, orientation):
        screen = rotatescreen.get_primary_display()
        if orientation == "landscape":
            screen.set_landscape()
            self.showMessage("Screen Orientation", "Changed to Landscape mode", QIcon('assets/round_screen_rotation_white_48dp.png'))
        elif orientation == "portrait":
            screen.set_portrait()
            self.showMessage("Screen Orientation", "Changed to Portrait mode", QIcon('assets/round_screen_rotation_white_48dp.png'))
        self.__update_actions_state()

    def __on_exit_callback(self):
        self.hide()
        keyboard.unhook_all()
        sys.exit()

    def __set_keyboard_hotkeys(self):
        keyboard.add_hotkey('ctrl+windows+alt+up', lambda: self.__on_orientation_change("landscape"), suppress=False)
        keyboard.add_hotkey('ctrl+windows+alt+down', lambda: self.__on_orientation_change("portrait"), suppress=False)


def main():
    app = QApplication(sys.argv)
    image = QIcon("assets/round_screen_rotation_white_48dp.png")

    tray_icon = TrayIcon(image)
    tray_icon.show()

    app.exec()
    keyboard.wait()


if __name__ == "__main__":
    main()
