# -----------------------------------------------------------
# Web Padlock
#
# (C) 2020 Reinoso Guzman, Madrid, Spain
# Released under MIT License
# -----------------------------------------------------------

import json
import logging
from flask import Flask, request
from flask_cors import CORS

from libs.systeminfo import get_systeminfo
from libs.config import get_config
from libs.metadata import get_metadata
from libs.jwt import load_private, load_cert, create_jwt


global config
global key
global cert

app = Flask(__name__)


@app.route('/')
def home():
    return json.dumps(get_metadata(), sort_keys=True, indent=4)


@app.route('/deviceinfo')
def deviceinfo():
    requestdata = {}
    for param in request.args.keys():
        requestdata[param] = request.args.get(param)

    token = create_jwt(
        key,
        cert,
        get_systeminfo(),
        get_metadata(),
        requestdata)

    return token


if __name__ == '__main__':

    config = get_config()
    logging.basicConfig(level=config["log_level"])

    key = load_private(config["private_key"])
    cert = load_cert(config["certificate"])

    CORS(app, origins=config["allowed_requesters"])

    app.run(host=config["listen_ip"],
            port=config["http_port"])
