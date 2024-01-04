import sys
import winreg
from pathlib import Path

from utils import variables as var


class Startup:
    def __init__(self):
        if sys.platform != 'win32':
            raise RuntimeError("This script is for Windows only")

        self.current_file_path = Path(sys.executable)
        self.program_name = var.APP_TITLE.replace(' ', '')
        self.program_path = str(self.current_file_path)
        self.key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    def __open_registry_key(self, access):
        return winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, access)

    def add_to_startup(self):
        with self.__open_registry_key(winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, self.program_name, 0, winreg.REG_SZ, self.program_path)

    def remove_from_startup(self):
        try:
            with self.__open_registry_key(winreg.KEY_WRITE) as key:
                winreg.DeleteValue(key, self.program_name)
        except FileNotFoundError:
            pass

    def get_registry_path(self) -> str | None:
        try:
            with self.__open_registry_key(winreg.KEY_READ) as key:
                value, _ = winreg.QueryValueEx(key, self.program_name)
                return value
        except FileNotFoundError:
            return None

    def update_registry_path(self):
        current_registry_path = self.get_registry_path()
        actual_file_path = str(Path(sys.executable))

        if current_registry_path is not None and current_registry_path != actual_file_path:
            with self.__open_registry_key(winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, self.program_name, 0, winreg.REG_SZ, actual_file_path)
