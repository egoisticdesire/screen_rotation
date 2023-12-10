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
        self.is_locked = False
        self.app_icon = QIcon(ICON_APP)
        self.setIcon(self.app_icon)
        self.setToolTip(TITLE_APP)

        self.primary_display = rotatescreen.get_primary_display()

        self.menu = RoundedCornersQMenu()
        self.menu.setWindowFlags(QtCore.Qt.WindowType.Popup)
        self.menu.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.orientation_group = QActionGroup(self)
        self.orientation_group.setExclusive(True)

        self.landscape_action = self.__create_action(TITLE_LANDSCAPE_MODE, ICON_LANDSCAPE_MODE, self.__on_orientation_change_callback, checkable=True)
        self.portrait_action = self.__create_action(TITLE_PORTRAIT_MODE, ICON_PORTRAIT_MODE, self.__on_orientation_change_callback, checkable=True)
        self.exit_action = self.__create_action(TITLE_EXIT, ICON_EXIT, self.__on_exit_callback)

        self.orientation_group.addAction(self.landscape_action)
        self.orientation_group.addAction(self.portrait_action)

        menu_actions = [self.landscape_action, self.portrait_action, self.menu.addSeparator(), self.exit_action]
        self.menu.addActions(menu_actions)

        self.setContextMenu(self.menu)

        # Установка начального состояния активности кнопок
        self.__update_actions_state()

        # Подключаем обработчик к событию клика по иконке в трее
        self.activated.connect(self.__tray_icon_activated)

    def __tray_icon_activated(self, reason):
        if reason == self.ActivationReason.Trigger:
            # Обработка одиночного клика
            if self.is_locked:
                self.setIcon(QIcon(ICON_APP))
                self.setToolTip(TITLE_APP)
                self.is_locked = False
            else:
                self.setIcon(QIcon('assets/round_screen_lock_rotation_white_48dp.png'))
                self.setToolTip(f'{TITLE_APP} :: LOCKED')
                self.is_locked = True
        elif reason == self.ActivationReason.DoubleClick:
            # Обработка двойного клика
            self.__on_orientation_change_callback()

    def __create_action(self, title, icon, callback, checkable=False):
        action = QAction(self)
        action.setText(title)
        action.setIcon(QIcon(icon))
        action.setCheckable(checkable)
        action.triggered.connect(callback)
        return action

    def __update_actions_state(self):
        current_orientation = self.primary_display.current_orientation

        # Проверка текущего режима экрана (0 - landscape, 90 - portrait)
        if current_orientation == 0:
            self.landscape_action.setChecked(True)
            self.landscape_action.setEnabled(False)
            self.portrait_action.setEnabled(True)
            set_hotkeys_to_landscape_mode(self.__on_orientation_change_callback)

        elif current_orientation == 90:
            self.portrait_action.setChecked(True)
            self.portrait_action.setEnabled(False)
            self.landscape_action.setEnabled(True)
            set_hotkeys_to_portrait_mode(self.__on_orientation_change_callback)

    def __on_orientation_change_callback(self):
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
