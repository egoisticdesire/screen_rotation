import sys
import winreg
from pathlib import Path

from utils import variables as var


class Startup:
    def __init__(self):
        if sys.platform != 'win32':
            raise RuntimeError("This script is for Windows only")

        self.current_file_path = Path(sys.executable)
        self.program_name = var.TITLES['app'].replace(' ', '')
        self.program_path = str(self.current_file_path)
        self.key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    def add_to_startup(self):
        # Открываем ключ реестра для записи
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_WRITE)
        # Устанавливаем значение ключа для добавления программы в автозагрузку
        winreg.SetValueEx(key, self.program_name, 0, winreg.REG_SZ, self.program_path)
        # Закрываем ключ реестра
        winreg.CloseKey(key)

    def remove_from_startup(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_WRITE)
            # Удаляем значение ключа для удаления программы из автозагрузки
            winreg.DeleteValue(key, self.program_name)
            winreg.CloseKey(key)

        except FileNotFoundError:
            pass

    def get_registry_path(self) -> str | None:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, self.program_name)
            winreg.CloseKey(key)
            return value

        except FileNotFoundError:
            return None

    def update_registry_path(self):
        current_registry_path = self.get_registry_path()
        actual_file_path = str(Path(sys.executable))

        if current_registry_path is not None and current_registry_path != actual_file_path:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, self.program_name, 0, winreg.REG_SZ, actual_file_path)
            winreg.CloseKey(key)
