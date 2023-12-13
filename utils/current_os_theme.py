import subprocess


def get_windows_color_scheme():
    try:
        cmd = 'powershell "Get-ItemPropertyValue -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name SystemUsesLightTheme"'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        output = result.stdout.strip()

        if output == '0':
            return 'dark_theme'
        elif output == '1':
            return 'light_theme'
        else:
            return 'unknown_theme'

    except Exception as e:
        return f'[ERROR] :: {str(e)}'

# def get_linux_gnome_color_scheme():
#     try:
#         cmd = 'gsettings get org.gnome.desktop.interface gtk-theme'
#         result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
#         theme = result.stdout.strip()
#         return theme
#     except Exception as e:
#         return f'Ошибка: {str(e)}'
#
#
# def get_linux_kde_color_scheme():
#     try:
#         cmd = 'kreadconfig5 --file ~/.config/kdeglobals --group General --key ColorScheme'
#         result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
#         theme = result.stdout.strip()
#         return theme
#     except Exception as e:
#         return f'Ошибка: {str(e)}'
#
#
# def get_linux_xfce_color_scheme():
#     try:
#         cmd = 'xfconf-query -c xsettings -p /Net/ThemeName'
#         result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
#         theme = result.stdout.strip()
#         return theme
#     except Exception as e:
#         return f'Ошибка: {str(e)}'
