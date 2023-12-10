import keyboard

from utils.variables import HOTKEY_LANDSCAPE_MODE, HOTKEY_PORTRAIT_MODE


def set_hotkeys_to_landscape_mode(orientation):
    keyboard.unhook_all()
    keyboard.add_hotkey(HOTKEY_LANDSCAPE_MODE, orientation, suppress=False)


def set_hotkeys_to_portrait_mode(orientation):
    keyboard.unhook_all()
    keyboard.add_hotkey(HOTKEY_PORTRAIT_MODE, orientation, suppress=False)
