# Remote server part

## Install

Requirements:

    pip install -r requirements.txt

## Run

### Server

    python server.py

### check_token.py

Validate a saved token.

    $ python check_token.py testtoken.dat
    eyhb...eFhjygH
    INFO:root:Decoding token ok
    INFO:root:Certificate verification OK
    INFO:root:System hostname matches certificate CN.
    Certificate data:
    {
        "cn": "workstation001",
        "issuer": "CN=CA Pruebas Intermediate,O=CA Pruebas,ST=Madrid,C=ES",
        "not_valid_after": "2021-10-23T09:21:30",
        "not_valid_before": "2020-10-13T09:21:30",
        "subject": "CN=workstation001,O=WebPadlock,C=ES"
    }

    Token claims:
    {
        "iat": 1602584381,
        "metadata": {
            "name": "Web Padlock",
            "tokenid": "rCVUaGCubecBGIJfyRZRveGJvoBUSyRnUUUPQKOM",
            "version": {
                "mayor": "1",
                "minor": "0"
            }
        },
        "requestdata": {
            "requestId": "f01253ff497eae7fa1555c34a822c2498835c58b"
        },
        "systeminfo": {
            "hostname": "workstation001",
            "osname": "Windows",
            "osrelease": "8.1",
            "osversion": "6.3.9600",
            "user": "Reinoso"
        }
    }

## Server endpoints

### /

Demo server's home page

### /check?token=

Return a status html message for the demo service.

### /jsoncheck?token=

Return raw information in JSON format. Then you can make all validations you want.

    {
        "token": {
            "claims": {
                "iat": 1602690016,
                "metadata": {
                    "name": "Web Padlock",
                    "tokenid": "KHHiHhbOpCRYBXQuRwrDVdlLMDBrBUEulhoMgsLI",
                    "version": {
                        "mayor": "1",
                        "minor": "0"
                    }
                },
                "requestdata": {
                    "requestId": "UrXiMGLvBeUSaTxNoHqv"
                },
                "systeminfo": {
                    "hostname": "hostname",
                    "osname": "Windows",
                    "osrelease": "8.1",
                    "osversion": "6.3.9600",
                    "user": "Reinoso"
                }
            },
            "validation": {
                "error": 0,
                "message": "Signature is valid"
            }
        },
        "x509": {
            "data": {
                "cn": "workstation001",
                "issuer": "CN=CA Pruebas Intermediate,O=CA Pruebas,ST=Madrid,C=ES",
                "not_valid_after": "2021-10-23T09:21:30",
                "not_valid_before": "2020-10-13T09:21:30",
                "subject": "CN=workstation001,O=WebPadlock,C=ES"
            },
            "validation": {
                "error": 0,
                "message": "Valid x509 certificate"
            }
        }
    }

## Todo

- improve documentation
- better looking website
