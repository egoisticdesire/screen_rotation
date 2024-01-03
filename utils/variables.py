from utils.current_os_theme import get_windows_color_scheme
from assets import resources

HOTKEY_LANDSCAPE_MODE = 'ctrl+alt+up'
HOTKEY_PORTRAIT_MODE = 'ctrl+alt+down'

LOCALHOST = '127.0.0.1'
PORT = 56565

TITLES = {
    'app': 'Screen Rotation',
    'app_lock': ' :: LOCKED',
    'landscape_mode': 'Landscape mode',
    'portrait_mode': 'Portrait mode',
    'screen_rotation_lock': 'Screen rotation locked',
    'quit': 'Quit',
    'startup_add': 'Add to startup',
    'startup_remove': 'Remove from startup',
}

MESSAGES = {
    'title': 'Screen Rotation',
    'landscape_mode': 'Changed to Landscape mode',
    'portrait_mode': 'Changed to Portrait mode',
    'startup_add': 'The application has been added to startup',
    'startup_remove': 'The application has been removed from startup',
    'already_running': 'The application is already running',
}

ICONS = {
    '_screen_rotation': f':icons/{get_windows_color_scheme()}_screen_rotation.png',
    '_screen_lock_rotation': f':icons/{get_windows_color_scheme()}_screen_lock_rotation.png',
    '_screen_landscape': f':icons/{get_windows_color_scheme()}_screen_landscape.png',
    '_screen_portrait': f':icons/{get_windows_color_scheme()}_screen_portrait.png',
    '_quit': f':icons/{get_windows_color_scheme()}_quit.png',
    '_startup_add': f':icons/{get_windows_color_scheme()}_startup_add.png',
    '_startup_remove': f':icons/{get_windows_color_scheme()}_startup_remove.png',
}

FONTS = {
    '_font': ':fonts/JetBrainsMonoRegular.ttf',
}
