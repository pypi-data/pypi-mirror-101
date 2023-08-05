import ctypes
import sys


def get_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        pass
    else:
        # rerun the script with admin right
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
