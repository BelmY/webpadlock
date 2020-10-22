import os
import sys
import getpass
import platform
import uuid


def get_systeminfo():
    """Return a dictionary with information about the host system.
    Pay attention to cross platform issues."""
    info = {
        "service_user": None,
        "hostname": None,
        "platform": None,
        "os": {
            "name": None,
            "release": None,
            "version": None,
        },
        "custom": None
    }

    # General info
    info["user"] = getpass.getuser()
    info["hostname"] = platform.node()
    info["macaddr"] = hex(uuid.getnode())
    info["platform"] = sys.platform

    # Related to OS and version
    info["os"]["name"] = platform.system()
    info["os"]["release"] = platform.release()
    info["os"]["version"] = platform.version()

    # Get additional system info depending on which os is running

    # python3 sys.platform values
    # ----------------------------
    # Linux          - linux
    # Windows        - win32
    # Windows/Cygwin - cygwin
    # Windows/MSYS2  - msys
    # Mac OS X       - darwin
    # OS/2           - os2
    # OS/2 EMX       - os2emx
    # RiscOS         - riscos
    # AtheOS         - atheos
    # FreeBSD 7      - freebsd7
    # FreeBSD 8      - freebsd8
    # FreeBSD N      - freebsdN
    # OpenBSD 6      - openbsd6

    return info


if __name__ == '__main__':
    import json
    print("System information claim will be:")
    print(json.dumps(get_systeminfo(), sort_keys=True, indent=4))
