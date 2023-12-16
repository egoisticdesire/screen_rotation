from utils.current_os_theme import get_windows_color_scheme
from assets import resources

HOTKEY_LANDSCAPE_MODE = 'ctrl+alt+up'
HOTKEY_PORTRAIT_MODE = 'ctrl+alt+down'

TITLES = {
    'app': 'Screen Rotation',
    'app_lock': ' :: LOCKED',
    'landscape_mode': 'Landscape mode',
    'portrait_mode': 'Portrait mode',
    'screen_rotation_locked': 'Screen rotation locked',
    'quit': 'Quit',
    'logging': 'screen_rotation.log',
}

MESSAGES = {
    'title': 'Screen Orientation',
    'landscape_mode': 'Changed to Landscape mode',
    'portrait_mode': 'Changed to Portrait mode',
}

ICONS = {
    '_screen_rotation': f':assets/{get_windows_color_scheme()}_screen_rotation.png',
    '_screen_lock_rotation': f':assets/{get_windows_color_scheme()}_screen_lock_rotation.png',
    '_screen_lock_landscape': f':assets/{get_windows_color_scheme()}_screen_lock_landscape.png',
    '_screen_lock_portrait': f':assets/{get_windows_color_scheme()}_screen_lock_portrait.png',
    '_quit': f':assets/{get_windows_color_scheme()}_quit.png',
}
