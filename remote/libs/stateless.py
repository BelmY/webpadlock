# Routines for stateless token: No session needed
import hmac
import hashlib
import time
from .randomstr import get_random_string


def new_auth_session(secret):
    """
    Create a new authorization session. Including:
     - nonce
     - server time
     - SHA-1 hmac signature of all data with the secret
    Return an object with vars identifing a new auth session.
    """

    data = {
        "nonce": None,
        "server_time": None,
        "signature": None
    }

    data["nonce"] = get_random_string(20)
    data["server_time"] = int(time.time())

    message = '{}{}'.format(
        data["nonce"],
        data["server_time"])

    signature = hmac.new(
        bytes(secret, 'latin-1'),
        msg=bytes(message, 'latin-1'),
        digestmod=hashlib.sha1)

    data["signature"] = signature.hexdigest()
    return data


def check_auth_session(data, secret):
    """
    Validates an authorization session's signature.
    Return elapsed time in seconds. None if it is invalid.
    """

    message = '{}{}'.format(
        data["nonce"],
        data["server_time"])

    signature = hmac.new(
        bytes(secret, 'latin-1'),
        msg=bytes(message, 'latin-1'),
        digestmod=hashlib.sha1)

    if signature.hexdigest() == data["signature"]:
        return int(time.time()) - int(data["server_time"])
    else:
        return None


if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: {} secret".format(sys.argv[0]))
        exit()

    secret = sys.argv[1]

    print("Auth session data with secret '{}':".format(secret))
    print(json.dumps(new_auth_session(secret), sort_keys=True, indent=4))
