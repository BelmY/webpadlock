# Utility files

## config.py

Read the configuration parameters and return then in a dict. Example:

    $ config.py
    Configuration dict:
    {
        "certificate": "workstation001-cert.pem",
        "log_level": 10,
        "private_key": "workstation001-key.pem"
    }

## systeminfo.py

Return information about specific platform the software is running. Like this:

    $ systeminfo.py
    System information claim will be:
    {
        "hostname": "worstation001",
        "osname": "Windows",
        "osrelease": "8.1",
        "osversion": "6.3.9600",
        "user": "user001"
    }

Note *user* is not the logged user, but the user running the daemon.

You can customize these fields in systeminfo.py.

## metadata.py

Return information about this software. As well as a random response identifier.

    $ metadata.py
    Metadata claim:
    {
        "name": "Web Padlock",
        "response-id": "HcxWRDKwdaScAypSczjiFWLpgTeIpOfGSiPduAjS",
        "version": {
            "mayor": "1",
            "minor": "0"
        }
    }

## jwt.py

Compose and sign the JWT.
