# Remote server part

You should remove the server demo endpoints before use it in production. **Only use the JSON API.**

## Install

Requirements:

    pip install -r requirements.txt

## Run

### Server

To start the server run

    python server.py

Or, as a WSGI application,

    gunicorn server:app

Don't forget to setup https in the server.

### check_token.py

CLI command to validate a saved token.

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

## Server API JSON

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

Return a JSON object with basic validations:

- token format
- token signature
- signing certificate
- session data

Then you can use this information to permit of deny access.

For example:

- check the signature is valid (token.validation.error = 0)
- check the certificate is valid (x509.validation.error = 0)
- check if the host name in system information matches the signing certificate's cn field. To prevent illegal copy of certificates
- check if the session elapsed time is less than 3 seconds. It makes impractical to retrieve a token from a compromised remote laptop.

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

## Server demo pages

### GET /

Demo server's home page

### GET /democheck?token=

Return a formated html message for the demo service.

## Configuration file

Example:

    {
        "cachain": [
            "intermediate.cert.pem",
            "ca.cert.pem"
        ],
        "http_port": 10000,
        "listen_ip": "0.0.0.0",
        "local_server_url": "http://127.0.0.1:3000/deviceinfo",
        "log_level": 10,
        "session_secret": "webpadlock"
    }

Parameters:

- cachain: array with all trusted certificates.
- local_server_url: url to ask for a local token in enrolled devices.
- log_level: log level (see python logging package levels)
- session_secret: key to calculate the stateless sessions
- http_port: listening port (for stand-alone server)
- listen_ip: binding interface (for stand-alone server)
