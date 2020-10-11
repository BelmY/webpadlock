# Web Padlock Local Server

This should be running in the user workstation/laptop.

## Install

Requirements:
 - jwcrypto
 - flask
 - platform
 - json

## Technical details

### JWT format

Claims example:

    {
      "metadata": {
        "name": "Web Padlock",
        "response-id": "bPvluRvVSJzfLOfKxXhsppOWMsebTqiRPRfNKaks",
        "version": {
          "mayor": "1",
          "minor": "0"
        }
      },
      "requestdata": {
        "nonce": "f01253ff497eae7fa1555c34a822c2498835c58b"
      },
      "systeminfo": {
        "hostname": "worstation0001",
        "osname": "Windows",
        "osrelease": "8.1",
        "osversion": "6.3.9600",
        "user": "username"
      }
    }

The claim `requestdata` is copied form the request. So the requester may put any arbitray data in it.


## TODO

 - web server
 - web server origin domains filter
 - cors headers
 - daemonize
 - certificate chain
 - check key permissions
 - integration with hardware TPM
