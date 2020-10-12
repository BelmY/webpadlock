# -----------------------------------------------------------
# Web Padlock demo server
#
# (C) 2020 Reinoso Guzman, Madrid, Spain
# Released under MIT License
# -----------------------------------------------------------

import json
import logging
from flask import Flask, request, render_template, session

from libs.config import get_config
from libs.randomstr import get_random_string
from libs.utils import load_file
from libs.jwt_checks import check_sign_cert

global config
global pemcacert


app = Flask(__name__,
            static_url_path='',
            static_folder="web/static",
            template_folder="web/templates")


@app.route('/')
def home():
    session['requestId'] = get_random_string(20)
    return render_template("index.html",
                           local_server_url=config["local_server_url"])


@app.route('/check')
def check():
    token = request.args.get("token")
    if (token is None):
        return ("Bad Request", 400)
    else:
        return webcheck(token)


def webcheck(token):
    return ("ok", 200)


if __name__ == '__main__':

    config = get_config()
    logging.basicConfig(level=config["log_level"])

    pemcacert = load_file(config["cacert"])
    logging.info("Loaded CA certificate from {}.".format(config["cacert"]))

    app.secret_key = config["session_secret"]
    app.run(host=config["listen_ip"],
            port=config["http_port"])
