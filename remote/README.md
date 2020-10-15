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

### GET /start_auth

Return a stateles authenticacion session. Like this:
    {
        "nonce": "fTZSEuHtEBPzzpWrgNEF",
        "server_time": "1602760264",
        "signature": "88bb5d9c099e9f4c683467a5f98d83c9df218df6"
    }

`Nonce` is a random string to prevent replay attacks.
`server_time` is the current server timestamp. It allows the server calculate the time elapsed from this session when the token arrives back to it.
And `signature` is a SHA1-HMAC function of the data above. The key is in configuration file.

You should call this endpoint just before request a token from the local agent. And don't forget include this variables in the request:

   http://127.0.0.1:3000/deviceinfo?nonce=...&server_time=...&signature=...


### GET /check?token=

Return a JSON object with basic validations. You can then add others validations you want.

The returned object is:

    {
        "session": {
            "elapsed": 29,
            "present": true
        },
        "token": {
            "claims": {
                "iat": 1602759941,
                "metadata": {
                    "name": "Web Padlock",
                    "tokenid": "JvJJMzusUAhzRNRTNefahxTlPvkDNtCjnEAhuUSB",
                    "version": {
                        "mayor": "1",
                        "minor": "0"
                    }
                },
                "requestdata": {
                    "nonce": "EjxHZFTutvCPPjrNlifK",
                    "server_time": "1602759912",
                    "signature": "0225e0b1fb5ca7c12216d40228cb580575bd47c1"
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

### GET /

Demo server's home page

### GET /democheck?token=

Return a formated html message for the demo service.

## Todo

- improve documentation
