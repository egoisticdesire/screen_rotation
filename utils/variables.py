from assets import resources
from utils.current_os_theme import get_windows_color_scheme
from utils.utils import get_system_lang, get_text

IS_RUS = get_system_lang().startswith('ru')

HOTKEY_LANDSCAPE_MODE = 'ctrl+alt+up'
HOTKEY_PORTRAIT_MODE = 'ctrl+alt+down'

LOCALHOST = '127.0.0.1'
PORT = 56565

_TITLES = {
    'app': {
        'en': 'Screen Rotation',
    },
    'app_lock': {
        'en': ' :: LOCKED',
        'ru': ' :: ЗАБЛОКИРОВАНО',
    },
    'landscape_mode': {
        'en': 'Landscape mode',
        'ru': 'Альбомный режим',
    },
    'portrait_mode': {
        'en': 'Portrait mode',
        'ru': 'Портретный режим',
    },
    'screen_rotation_lock': {
        'en': 'Screen rotation locked',
        'ru': 'Поворот экрана заблокирован',
    },
    'quit': {
        'en': 'Quit',
        'ru': 'Выход',
    },
    'startup_add': {
        'en': 'Add to startup',
        'ru': 'Добавить в автозагрузку',
    },
    'startup_remove': {
        'en': 'Remove from startup',
        'ru': 'Удалить из автозагрузки',
    },
}
_MESSAGES = {
    'landscape_mode': {
        'en': 'Changed to Landscape mode',
        'ru': 'Переключено на альбомный режим',
    },
    'portrait_mode': {
        'en': 'Changed to Portrait mode',
        'ru': 'Переключено на портретный режим',
    },
    'startup_added': {
        'en': 'The application has been added to startup',
        'ru': 'Приложение добавлено в автозагрузку',
    },
    'startup_removed': {
        'en': 'The application has been removed from startup',
        'ru': 'Приложение удалено из автозагрузки',
    },
    'already_running': {
        'en': 'The application is already running',
        'ru': 'Приложение уже запущено',
    },
}

APP_TITLE = get_text(_TITLES, 'app')
APP_LOCK_TITLE = get_text(_TITLES, 'app_lock', 'ru' if IS_RUS else 'en')
LANDSCAPE_MODE_TITLE = get_text(_TITLES, 'landscape_mode', 'ru' if IS_RUS else 'en')
PORTRAIT_MODE_TITLE = get_text(_TITLES, 'portrait_mode', 'ru' if IS_RUS else 'en')
SCREEN_ROTATION_LOCK_TITLE = get_text(_TITLES, 'screen_rotation_lock', 'ru' if IS_RUS else 'en')
QUIT_TITLE = get_text(_TITLES, 'quit', 'ru' if IS_RUS else 'en')
STARTUP_ADD_TITLE = get_text(_TITLES, 'startup_add', 'ru' if IS_RUS else 'en')
STARTUP_REMOVE_TITLE = get_text(_TITLES, 'startup_remove', 'ru' if IS_RUS else 'en')

LANDSCAPE_MODE_MESSAGE = get_text(_MESSAGES, 'landscape_mode', 'ru' if IS_RUS else 'en')
PORTRAIT_MODE_MESSAGE = get_text(_MESSAGES, 'portrait_mode', 'ru' if IS_RUS else 'en')
STARTUP_ADDED_MESSAGE = get_text(_MESSAGES, 'startup_added', 'ru' if IS_RUS else 'en')
STARTUP_REMOVED_MESSAGE = get_text(_MESSAGES, 'startup_removed', 'ru' if IS_RUS else 'en')
APP_ALREADY_RUNNING_MESSAGE = get_text(_MESSAGES, 'already_running', 'ru' if IS_RUS else 'en')

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
