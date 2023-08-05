"""
Utility functions for desktop integration on linux and windows
"""
import sys
import os
import ptk_lib.resources


def get_menu_folder():
    """
    Get menu folder
    """
    if sys.platform == 'linux':
        return linux_get_menu_folder()

    elif sys.platform.startswith('win'):
        return win_get_menu_folder()

def linux_get_menu_foler():
    """
    Get menu folder on linux
    """
    return os.path.join(os.path.join(os.path.expanduser('~')), '.local', 'share', 'applications')

def linux_create_shortcut_file(target_name, target_path, shortcut_directory):
        """
        Creates a Linux shortcut file.
        """
        shortcut_file_path = os.path.join(shortcut_directory, "launch_" + target_name + ".desktop")
        with open(shortcut_file_path, "w") as shortcut:
            shortcut.write("[Desktop Entry]\n")
            shortcut.write("Name={}\n".format(target_name))
            shortcut.write("Exec={}\n".format(target_path))
            shortcut.write("Icon="+ptk_lib.resources.__path__[0]+"ptkicon.svg\n")
            shortcut.write("Type=Application\n")
            shortcut.write("Terminal=false\n")
            shortcut.write("Categories=Education;Programming\n")

            # make the launch file executable
            st = os.stat(shortcut_file_path)
            os.chmod(shortcut_file_path, st.st_mode | stat.S_IEXEC)
        
        return shortcut_file_path

