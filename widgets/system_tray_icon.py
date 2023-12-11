import sys

import keyboard
import rotatescreen
from PyQt6 import QtCore, QtWidgets, QtGui

from utils import variables as var
from utils.utils import set_hotkeys_to_landscape_mode, set_hotkeys_to_portrait_mode
from widgets.rounded_menu import RoundedCornersQMenu


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_locked = False
        self.app_icon = QtGui.QIcon(var.ICON_APP)
        self.setIcon(self.app_icon)
        self.setToolTip(var.TITLE_APP)

        self.primary_display = rotatescreen.get_primary_display()
        # self.secondary_displays = rotatescreen.get_secondary_displays()

        self.menu = RoundedCornersQMenu()
        self.menu.setWindowFlags(QtCore.Qt.WindowType.Popup)
        self.menu.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.orientation_group = QtGui.QActionGroup(self)
        self.orientation_group.setExclusive(True)

        self.landscape_action = self.__create_action(
            title=var.TITLE_LANDSCAPE_MODE,
            icon=var.ICON_LANDSCAPE_MODE,
            callback=self.__on_orientation_change_callback,
            set_shortcut=var.HOTKEY_LANDSCAPE_MODE,
            is_shortcut_visible=True,
            checkable=True,
        )
        self.portrait_action = self.__create_action(
            title=var.TITLE_PORTRAIT_MODE,
            icon=var.ICON_PORTRAIT_MODE,
            callback=self.__on_orientation_change_callback,
            set_shortcut=var.HOTKEY_PORTRAIT_MODE,
            is_shortcut_visible=True,
            checkable=True,
        )
        self.screen_rotation_locked = self.__create_action(
            title=var.TITLE_SCREEN_ROTATION_LOCKED,
            icon=var.ICON_APP_LOCK,
            is_enabled=False,
            is_visible=False,
        )
        self.quit_action = self.__create_action(
            title=var.TITLE_QUIT,
            icon=var.ICON_QUIT,
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

    def __update_actions_state(self):
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

    def __create_action(
        self,
        title: str,
        icon: str,
        callback: callable = None,
        checkable: bool = False,
        is_enabled: bool = True,
        is_visible: bool = True,
        set_shortcut: str = '',
        is_shortcut_visible: bool = False,
    ):
        action = QtGui.QAction(self)
        action.setText(title)
        action.setIcon(QtGui.QIcon(icon))
        action.setCheckable(checkable)
        action.setShortcut(set_shortcut)
        action.setShortcutVisibleInContextMenu(is_shortcut_visible)
        action.setEnabled(is_enabled)
        action.setVisible(is_visible)
        if callback is not None:
            action.triggered.connect(callback)
        return action

    def __lock_orientation(self):
        self.setIcon(QtGui.QIcon(var.ICON_APP_LOCK))
        self.setToolTip(f'{var.TITLE_APP}{var.TITLE_APP_LOCK}')

        self.landscape_action.setVisible(False)
        self.portrait_action.setVisible(False)
        self.screen_rotation_locked.setVisible(True)

        keyboard.unhook_all()
        self.is_locked = True

    def __unlock_orientation(self):
        self.setIcon(QtGui.QIcon(var.ICON_APP))
        self.setToolTip(var.TITLE_APP)

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
        orientation = self.primary_display.current_orientation

        if orientation == 0:
            self.primary_display.set_portrait()
            self.showMessage(var.MESSAGE_TITLE, var.MESSAGE_PORTRAIT_MODE, self.app_icon)

        elif orientation == 90:
            self.primary_display.set_landscape()
            self.showMessage(var.MESSAGE_TITLE, var.MESSAGE_LANDSCAPE_MODE, self.app_icon)

        self.__update_actions_state()

    def __on_quit_callback(self):
        self.hide()
        keyboard.unhook_all()
        sys.exit()
