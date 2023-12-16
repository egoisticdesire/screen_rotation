import sys

import keyboard
import rotatescreen
from PyQt6 import QtCore, QtWidgets, QtGui

from utils import variables as var
from utils.current_os_theme import get_windows_color_scheme
from utils.logger import Logger
from utils.themes import set_dark_theme, set_light_theme
from utils.utils import create_action, set_hotkeys_to_landscape_mode, set_hotkeys_to_portrait_mode
from widgets.rounded_menu import RoundedCornersQMenu

LOGGER = Logger(name=__name__)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_locked = False
        self.icons = var.ICONS
        self.app_icon = QtGui.QIcon(self.icons['_screen_rotation'])
        self.setIcon(self.app_icon)
        self.setToolTip(var.TITLES['app'])

        self.current_os_theme = get_windows_color_scheme()
        self.primary_display = rotatescreen.get_primary_display()
        # self.secondary_displays = rotatescreen.get_secondary_displays()

        self.menu = RoundedCornersQMenu()
        self.menu.setWindowFlags(QtCore.Qt.WindowType.Popup)
        self.menu.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.orientation_group = QtGui.QActionGroup(self)
        self.orientation_group.setExclusive(True)

        self.landscape_action = create_action(
            title=var.TITLES['landscape_mode'],
            icon=self.icons['_screen_lock_landscape'],
            callback=self.__on_orientation_change_callback,
            set_shortcut=var.HOTKEY_LANDSCAPE_MODE,
            is_shortcut_visible=True,
            checkable=True,
        )
        self.portrait_action = create_action(
            title=var.TITLES['portrait_mode'],
            icon=self.icons['_screen_lock_portrait'],
            callback=self.__on_orientation_change_callback,
            set_shortcut=var.HOTKEY_PORTRAIT_MODE,
            is_shortcut_visible=True,
            checkable=True,
        )
        self.screen_rotation_locked = create_action(
            title=var.TITLES['screen_rotation_locked'],
            icon=self.icons['_screen_lock_rotation'],
            is_enabled=False,
            is_visible=False,
        )
        self.quit_action = create_action(
            title=var.TITLES['quit'],
            icon=self.icons['_quit'],
            callback=self.__on_quit_callback
        )

        self.orientation_group.addAction(self.landscape_action)
        self.orientation_group.addAction(self.portrait_action)

        menu_actions = [
            self.landscape_action,
            self.portrait_action,
            self.screen_rotation_locked,
            self.menu.addSeparator(),
            self.quit_action,
        ]
        self.menu.addActions(menu_actions)
        self.setContextMenu(self.menu)

        self.__update_actions_state()

        self.activated.connect(self.__on_tray_icon_activated_callback)

        # Создание таймера для отслеживания изменений
        self.timer_change_theme = QtCore.QTimer(self)
        self.timer_change_theme.timeout.connect(lambda: self.menu.setStyleSheet(self.__check_os_theme()))
        self.timer_change_theme.timeout.connect(self.__refresh_primary_display_info)
        self.timer_change_theme.start(1000)

    def __refresh_primary_display_info(self):
        try:
            self.primary_display = rotatescreen.get_primary_display()
            # self.secondary_displays = rotatescreen.get_secondary_displays()
            # Обновите остальные данные или параметры, которые могли измениться
        except Exception as e:
            LOGGER.log_error(f'An error occurred while refreshing the primary display information: {e}')

    def __check_os_theme(self):
        os_theme = get_windows_color_scheme()
        new_stylesheet = set_dark_theme(self.menu.radius) if os_theme == 'dark_theme' else set_light_theme(self.menu.radius)

        # Проверка изменения темы и обновление иконки, если необходимо
        if os_theme != self.current_os_theme:
            self.__update_icons()
            self.current_os_theme = os_theme

        return new_stylesheet

    def __update_icons(self):
        for key in self.icons:
            self.icons[key] = f':assets/{get_windows_color_scheme()}{key}.png'

        if self.is_locked:
            self.setIcon(QtGui.QIcon(self.icons['_screen_lock_rotation']))
        else:
            self.setIcon(QtGui.QIcon(self.icons['_screen_rotation']))

        self.landscape_action.setIcon(QtGui.QIcon(self.icons['_screen_lock_landscape']))
        self.portrait_action.setIcon(QtGui.QIcon(self.icons['_screen_lock_portrait']))
        self.quit_action.setIcon(QtGui.QIcon(self.icons['_quit']))
        self.screen_rotation_locked.setIcon(QtGui.QIcon(self.icons['_screen_lock_rotation']))

    def __update_actions_state(self):
        try:
            orientation = self.primary_display.current_orientation

            if orientation == 0:
                self.landscape_action.setChecked(True)
                self.landscape_action.setEnabled(False)
                self.portrait_action.setEnabled(True)
                set_hotkeys_to_landscape_mode(self.__on_orientation_change_callback)

            elif orientation == 90:
                self.portrait_action.setChecked(True)
                self.portrait_action.setEnabled(False)
                self.landscape_action.setEnabled(True)
                set_hotkeys_to_portrait_mode(self.__on_orientation_change_callback)

        except Exception as e:
            LOGGER.log_error(f'An error occurred while updating actions state: {e}')

    def __lock_orientation(self):
        self.setIcon(QtGui.QIcon(self.icons['_screen_lock_rotation']))
        self.setToolTip(f"{var.TITLES['app']}{var.TITLES['app_lock']}")

        self.landscape_action.setVisible(False)
        self.portrait_action.setVisible(False)
        self.screen_rotation_locked.setVisible(True)

        keyboard.unhook_all()
        self.is_locked = True

    def __unlock_orientation(self):
        self.setIcon(QtGui.QIcon(self.icons['_screen_rotation']))
        self.setToolTip(var.TITLES['app'])

        self.landscape_action.setVisible(True)
        self.portrait_action.setVisible(True)
        self.screen_rotation_locked.setVisible(False)

        self.__update_actions_state()
        self.is_locked = False

    def __on_tray_icon_activated_callback(self, reason: QtWidgets.QSystemTrayIcon.ActivationReason):
        if reason == self.ActivationReason.Trigger:
            if self.is_locked:
                self.__unlock_orientation()
            else:
                self.__lock_orientation()

    def __on_orientation_change_callback(self):
        try:
            orientation = self.primary_display.current_orientation

            if orientation == 0:
                self.primary_display.set_portrait()
                # self.showMessage(var.MESSAGES['title'], var.MESSAGES['portrait_mode'], self.app_icon)

            elif orientation == 90:
                self.primary_display.set_landscape()
                # self.showMessage(var.MESSAGES['title'], var.MESSAGES['landscape_mode'], self.app_icon)

            self.__update_actions_state()

        except Exception as e:
            LOGGER.log_error(f'An error occurred while changing the screen orientation: {e}')

    def __on_quit_callback(self):
        self.hide()
        keyboard.unhook_all()
        sys.exit()
