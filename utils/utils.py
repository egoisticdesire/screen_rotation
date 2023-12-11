import keyboard

from utils import variables as var


def set_hotkeys_to_landscape_mode(orientation):
    keyboard.unhook_all()
    keyboard.add_hotkey(var.HOTKEY_PORTRAIT_MODE, orientation, suppress=False)


def set_hotkeys_to_portrait_mode(orientation):
    keyboard.unhook_all()
    keyboard.add_hotkey(var.HOTKEY_LANDSCAPE_MODE, orientation, suppress=False)
