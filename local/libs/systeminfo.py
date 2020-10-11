import os
import platform


def get_systeminfo():
    """Return a dictionary with information about the host system.
    Pay attention to cross platform issues."""
    info = {}
    info["hostname"] = platform.node()
    info["user"] = os.getlogin()
    info["osname"] = platform.system()
    info["osrelease"] = platform.release()
    info["osversion"] = platform.version()
    return info


if __name__ == '__main__':
    import json
    print("System information claim will be:")
    print(json.dumps(get_systeminfo(), sort_keys=True, indent=4))
