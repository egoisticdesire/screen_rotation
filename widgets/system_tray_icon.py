import sys
from pathlib import Path

import keyboard
import rotatescreen
from PyQt6 import QtCore, QtWidgets, QtGui

from utils import variables as var
from utils.current_os_theme import get_windows_color_scheme
from utils.logger import Logger
from utils.startup import Startup
from styles.tray_icon_themes import set_dark_theme, set_light_theme
from utils.utils import create_action, get_system_lang, set_hotkeys_to_landscape_mode, set_hotkeys_to_portrait_mode
from widgets.rounded_menu import RoundedCornersQMenu

LOGGER = Logger(name=__name__)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.startup = Startup()
        self.is_locked = False
        self.app_icon = QtGui.QIcon(var.ICONS['_screen_rotation'])
        self.setIcon(self.app_icon)
        self.setToolTip(var.APP_TITLE)

        self.current_os_theme = get_windows_color_scheme()
        self.primary_display = rotatescreen.get_primary_display()
        # self.secondary_displays = rotatescreen.get_secondary_displays()

        self.menu = RoundedCornersQMenu()
        self.menu.setWindowFlags(QtCore.Qt.WindowType.Popup)
        self.menu.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.menu.setStyleSheet(self.__update_menu_theme())

        self.orientation_group = QtGui.QActionGroup(self)
        self.orientation_group.setExclusive(True)

        self.landscape_action = create_action(
            title=var.LANDSCAPE_MODE_TITLE,
            icon=var.ICONS['_screen_landscape'],
            callback=self.__on_orientation_change_callback,
            set_shortcut=var.HOTKEY_LANDSCAPE_MODE,
            is_shortcut_visible=True,
            checkable=True,
        )
        self.portrait_action = create_action(
            title=var.PORTRAIT_MODE_TITLE,
            icon=var.ICONS['_screen_portrait'],
            callback=self.__on_orientation_change_callback,
            set_shortcut=var.HOTKEY_PORTRAIT_MODE,
            is_shortcut_visible=True,
            checkable=True,
        )
        self.screen_rotation_locked = create_action(
            title=var.SCREEN_ROTATION_LOCK_TITLE,
            icon=var.ICONS['_screen_lock_rotation'],
            is_enabled=False,
            is_visible=False,
        )
        self.quit_action = create_action(
            title=var.QUIT_TITLE,
            icon=var.ICONS['_quit'],
            callback=self.__on_quit_callback
        )
        self.startup_action = create_action(
            title=var.STARTUP_ADD_TITLE,
            icon=var.ICONS['_startup_add'],
            callback=self.__manage_startup_state,
            checkable=True,
        )

        self.orientation_group.addAction(self.landscape_action)
        self.orientation_group.addAction(self.portrait_action)

        menu_actions = [
            self.landscape_action,
            self.portrait_action,
            self.screen_rotation_locked,
            self.menu.addSeparator(),
            self.startup_action,
            self.menu.addSeparator(),
            self.quit_action,
        ]
        self.menu.addActions(menu_actions)
        self.setContextMenu(self.menu)

        self.__update_action_states()
        self.__update_startup_state()

        self.activated.connect(self.__on_tray_icon_activated_callback)

        # Создание таймера для отслеживания изменений
        self.updater = QtCore.QTimer(self)
        self.updater.timeout.connect(lambda: self.menu.setStyleSheet(self.__update_menu_theme()))
        self.updater.timeout.connect(self.__update_primary_display_info)
        self.updater.timeout.connect(self.startup.update_registry_path)
        self.updater.timeout.connect(self.__update_startup_state)
        self.updater.timeout.connect(lambda: get_system_lang())
        self.updater.start(1000)

    def __update_primary_display_info(self):
        try:
            self.primary_display = rotatescreen.get_primary_display()
            # self.secondary_displays = rotatescreen.get_secondary_displays()
        except Exception as e:
            LOGGER.log_error(f'Error while updating primary display information: {e}')

    def __update_menu_theme(self):
        os_theme = get_windows_color_scheme()
        new_stylesheet = set_dark_theme(self.menu.radius) if os_theme == 'dark_theme' else set_light_theme(self.menu.radius)

        # Проверка изменения темы и обновление иконки, если необходимо
        if os_theme != self.current_os_theme:
            self.__update_action_icons()
            self.current_os_theme = os_theme

        return new_stylesheet

    def __update_action_icons(self):
        for key in var.ICONS:
            var.ICONS[key] = f':icons/{get_windows_color_scheme()}{key}.png'

        app_icon = var.ICONS['_screen_lock_rotation'] if self.is_locked else var.ICONS['_screen_rotation']
        self.setIcon(QtGui.QIcon(app_icon))
        startup_action_icon = var.ICONS['_startup_remove'] if self.startup_action.isChecked() else var.ICONS['_startup_add']
        self.startup_action.setIcon(QtGui.QIcon(startup_action_icon))

        self.landscape_action.setIcon(QtGui.QIcon(var.ICONS['_screen_landscape']))
        self.portrait_action.setIcon(QtGui.QIcon(var.ICONS['_screen_portrait']))
        self.quit_action.setIcon(QtGui.QIcon(var.ICONS['_quit']))
        self.screen_rotation_locked.setIcon(QtGui.QIcon(var.ICONS['_screen_lock_rotation']))

    def __update_action_states(self):
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
        self.setIcon(QtGui.QIcon(var.ICONS['_screen_lock_rotation']))
        self.setToolTip(f"{var.APP_TITLE}{var.APP_LOCK_TITLE}")

        self.landscape_action.setVisible(False)
        self.portrait_action.setVisible(False)
        self.screen_rotation_locked.setVisible(True)

        keyboard.unhook_all()
        self.is_locked = True

    def __unlock_orientation(self):
        self.setIcon(QtGui.QIcon(var.ICONS['_screen_rotation']))
        self.setToolTip(var.APP_TITLE)

        self.landscape_action.setVisible(True)
        self.portrait_action.setVisible(True)
        self.screen_rotation_locked.setVisible(False)

        self.__update_action_states()
        self.is_locked = False

    def __update_startup_state(self):
        try:
            actual_file_path = str(Path(sys.executable))
            registry_path = self.startup.get_registry_path()

            if registry_path and registry_path == actual_file_path:
                self.startup_action.setChecked(True)
                self.__manage_startup_state()

        except Exception as e:
            LOGGER.log_error(f'An error occurred while refreshing startup actions state: {e}')

    def __manage_startup_state(self):
        registry_path = self.startup.get_registry_path()

        if self.startup_action.isChecked():
            self.startup_action.setText(var.STARTUP_REMOVE_TITLE)
            self.startup_action.setIcon(QtGui.QIcon(var.ICONS['_startup_remove']))
            # self.showMessage(None, var.STARTUP_ADDED_MESSAGE, self.app_icon)
            if not registry_path:
                self.startup.add_to_startup()

        else:
            self.startup_action.setText(var.STARTUP_ADD_TITLE)
            self.startup_action.setIcon(QtGui.QIcon(var.ICONS['_startup_add']))
            # self.showMessage(None, var.STARTUP_REMOVED_MESSAGE, self.app_icon)
            if registry_path:
                self.startup.remove_from_startup()

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
                # self.showMessage(None, var.PORTRAIT_MODE_MESSAGE, self.app_icon)

            elif orientation == 90:
                self.primary_display.set_landscape()
                # self.showMessage(None, var.LANDSCAPE_MODE_MESSAGE, self.app_icon)

            self.__update_action_states()

        except Exception as e:
            LOGGER.log_error(f'An error occurred while changing the screen orientation: {e}')

    def __on_quit_callback(self):
        self.hide()
        keyboard.unhook_all()
        sys.exit()
