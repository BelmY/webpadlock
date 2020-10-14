# Web Padlock Local Server

This should be running in the user workstation/laptop.

## Run this local agent

### From binary

Go to [latest release](https://github.com/electronicayciencia/webpadlock/releases) and download these files:

- **server.exe**: local agent.
- **config.json**: configuration file
- **workstation001.key.pem** and **workstation001.key.pem** example host certificates.

Put all of them in the same folder and run `server.exe`.

### From source

Install requirements:

    pip install -r requirements.txt

Run `server.py`.

## API endpoints

### Root (/)

Return a json with metadata. See below *metadata claim*.

### Device information (/deviceinfo)

Return a JWT with information, signed with private key. Arbitrary parameters. For example:

    http://127.0.0.1:3000/deviceinfo?nonce=ggg&timestamp=yyy

Will return the following JWT.

#### JWT header

The header contains the algorithm (RSA, SHA-256) and the host certificate chain. Being the first certificate the one used in signing operation.
The certificate's CN must match the hostname. And its private key must not be user readable.

    {
      "alg": "RS256",
      "x5c": ["MIIDa...8C7t"]
    }

#### JWT claims

The claims have three parts:

- **metadata**: Return information about this software. As well as a random response identifier.
- **requestdata**: Copy of request's arguments. Any parameter the requester puts on the request. Like nonce, requestid, timestamp, etc.
- **systeminfo**: Information about the system (os version, hostname, etc)

Example:

    {
      "metadata": {
        "name": "Web Padlock",
        "response-id": "OhRtVffSGMdvoePjmEoxdYNdMRoxMERatUkfKMwu",
        "version": {
          "mayor": "1",
          "minor": "0"
        }
      },
      "requestdata": {
        "nonce": "ggg",
        "timestamp": "yyy"
      },
      "systeminfo": {
        "hostname": "workstation001",
        "osname": "Windows",
        "osrelease": "8.1",
        "osversion": "6.3.9600",
        "user": "user001"
      }
    }

## TODO

- document config options
- daemonize
- check key permissions
- integration with hardware TPM
