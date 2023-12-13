import keyboard
from PyQt6 import QtGui

from utils import variables as var


def set_hotkeys_to_landscape_mode(orientation):
    keyboard.unhook_all()
    keyboard.add_hotkey(var.HOTKEY_PORTRAIT_MODE, orientation, suppress=False)


def set_hotkeys_to_portrait_mode(orientation):
    keyboard.unhook_all()
    keyboard.add_hotkey(var.HOTKEY_LANDSCAPE_MODE, orientation, suppress=False)


def create_action(
    title: str,
    icon: str,
    callback: callable = None,
    checkable: bool = False,
    is_enabled: bool = True,
    is_visible: bool = True,
    set_shortcut: str = '',
    is_shortcut_visible: bool = False,
):
    action = QtGui.QAction()
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
