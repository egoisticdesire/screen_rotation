import sys

import keyboard
import rotatescreen
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon
from PyQt6.QtGui import QAction, QActionGroup, QIcon

from utils.utils import set_hotkeys_to_landscape_mode, set_hotkeys_to_portrait_mode
from utils.variables import ICON_APP, ICON_EXIT, ICON_LANDSCAPE_MODE, ICON_PORTRAIT_MODE, MESSAGE_LANDSCAPE_MODE, MESSAGE_PORTRAIT_MODE, MESSAGE_TITLE, TITLE_APP, TITLE_EXIT, TITLE_LANDSCAPE_MODE, TITLE_PORTRAIT_MODE
from widgets.rounded_menu import RoundedCornersQMenu


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app_icon = QIcon(ICON_APP)
        self.setIcon(self.app_icon)
        self.setToolTip(TITLE_APP)

        self.primary_display = rotatescreen.get_primary_display()

        self.menu = RoundedCornersQMenu()
        self.menu.setWindowFlags(QtCore.Qt.WindowType.Popup)
        self.menu.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.orientation_group = QActionGroup(self)
        self.orientation_group.setExclusive(True)

        self.normal_action = self.__create_action(TITLE_LANDSCAPE_MODE, ICON_LANDSCAPE_MODE, self.__on_orientation_change, checkable=True)
        self.portrait_action = self.__create_action(TITLE_PORTRAIT_MODE, ICON_PORTRAIT_MODE, self.__on_orientation_change, checkable=True)
        self.quit_action = self.__create_action(TITLE_EXIT, ICON_EXIT, self.__on_exit_callback)

        self.orientation_group.addAction(self.normal_action)
        self.orientation_group.addAction(self.portrait_action)

        menu_actions = [self.normal_action, self.portrait_action, self.menu.addSeparator(), self.quit_action]
        self.menu.addActions(menu_actions)

        self.setContextMenu(self.menu)

        self.__update_actions_state()  # Установка начального состояния активности кнопок

    def __create_action(self, text, icon, callback, checkable=False):
        action = QAction(self)
        action.setText(text)
        action.setIcon(QIcon(icon))
        action.setCheckable(checkable)
        action.triggered.connect(callback)
        return action

    def __update_actions_state(self):
        # Проверка текущего режима экрана (0 - landscape, 90 - portrait)
        current_orientation = self.primary_display.current_orientation

        if current_orientation == 0:
            self.normal_action.setChecked(True)
            self.normal_action.setEnabled(False)
            self.portrait_action.setEnabled(True)
            set_hotkeys_to_landscape_mode(self.__on_orientation_change)

        elif current_orientation == 90:
            self.portrait_action.setChecked(True)
            self.portrait_action.setEnabled(False)
            self.normal_action.setEnabled(True)
            set_hotkeys_to_portrait_mode(self.__on_orientation_change)

    def __on_orientation_change(self):
        current_orientation = self.primary_display.current_orientation

        if current_orientation == 0:
            self.primary_display.set_portrait()
            self.showMessage(MESSAGE_TITLE, MESSAGE_PORTRAIT_MODE, self.app_icon)

        elif current_orientation == 90:
            self.primary_display.set_landscape()
            self.showMessage(MESSAGE_TITLE, MESSAGE_LANDSCAPE_MODE, self.app_icon)

        self.__update_actions_state()

    def __on_exit_callback(self):
        self.hide()
        keyboard.unhook_all()
        sys.exit()


def main():
    app = QApplication(sys.argv)

    tray_icon = SystemTrayIcon()
    tray_icon.show()

    app.exec()
    keyboard.wait()


if __name__ == "__main__":
    main()
