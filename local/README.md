# Web Padlock Local Server

This should be running in the user workstation/laptop.

## Technical details

### JWT format

    {
      "metadata": {
        "version": {
          "mayor": "1",
          "minor": "0"
        }
      },
      "requestdata": {
        "nonce": "f01253ff497eae7fa1555c34a822c2498835c58b"
      },
      "systeminfo": {
        "hostname": "workstation001"
      }
    }


The claim `requestdata` is copied form the request. So the requester may put any arbitray data in it.


TODO:
 - web server
 - web server origin filter
 - cors headers
 - separate files
 - daemonize
 - certificate chain
 - check key permissions
