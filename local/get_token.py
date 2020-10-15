import json
from jwcrypto import jwk, jwt
from jwcrypto.common import json_encode
import logging

from libs.systeminfo import get_systeminfo
from libs.config import get_config
from libs.metadata import get_metadata
from libs.jwt import load_private, load_cert, create_jwt

cfgfile = "config.json"


def run():
    """Usage demo"""
    config = get_config(cfgfile)

    logging.basicConfig(level=config["log_level"])

    key = load_private(config["private_key"])
    cert = load_cert(config["certificate"])

    requestdata = {
        "nonce": "ZmGRFsniiPfDBxCewuBO",
        "server_time": 1602753369,
        "signature": "851e8ce1f3df8c40390cef3664d9b5b9575946a9"
    }

    token = create_jwt(
        key,
        cert,
        get_systeminfo(),
        get_metadata(),
        requestdata)

    print(token)


if __name__ == '__main__':
    run()
