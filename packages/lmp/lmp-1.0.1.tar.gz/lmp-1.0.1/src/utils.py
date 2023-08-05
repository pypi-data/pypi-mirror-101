import errno
import platform
import sys
import signal
import os

def get_plat():
    plat = platform.system()
    if plat == "Darwin":
        return "macOS"
    elif plat == "Windows":
        return "windows"
    elif plat == "Linux":
        return "linux"
    else:
        sys.exit("Unknown OS, please report. 0-0")

def __exit(message: str):
    sys.exit(message)

def is_pathname_valid(pathname: str) -> bool:
    ERROR_INVALID_NAME = 123
    try:
        if not isinstance(pathname, str) or not pathname:
            return False
        _, pathname = os.path.splitdrive(pathname)

        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law

        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
           
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError as exc:
        return False
    else:
        return True