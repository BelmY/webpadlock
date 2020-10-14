# -----------------------------------------------------------
# Web Padlock demo server
#
# (C) 2020 Reinoso Guzman, Madrid, Spain
# Released under MIT License
# -----------------------------------------------------------

import json
import time
import logging
from flask import Flask, request, render_template, session

from libs.config import get_config
from libs.randomstr import get_random_string
from libs.utils import load_file
from libs.jwtchecks import process_token

global config
global pem_ca_chain

app = Flask(__name__,
            static_url_path='',
            static_folder="web/static",
            template_folder="web/templates")


@app.route('/')
def home():
    session['requestId'] = get_random_string(20)
    session['timeof'] = int(time.time())
    return render_template("index.html",
                           local_server_url=config["local_server_url"])


@app.route('/check')
def check():
    token = request.args.get("token")
    if (token is None):
        return ("Bad Request", 400)
    else:
        msg, status = webcheck(token)
        html_message = ""
        html_message += "<br>".join(msg)
        html_message += "<br>"
        return html_message, status


@app.route('/jsoncheck')
def jsoncheck():
    token = request.args.get("token")
    if (token is None):
        return ("Bad Request", 400)
    else:
        token_info = process_token(token, pem_ca_chain)
        return json.dumps(token_info), 200


def webcheck(token):
    """
    Compose a status message after the received token.
    This is only an example.
    """

    msg = []
    status = 200

    token_info = process_token(token, pem_ca_chain)

    # Check token signature
    if token_info["token"]["validation"]["error"] == 0:
        msg.append("INFO: " + token_info["token"]["validation"]["message"])
    else:
        msg.append("CRITICAL" + token_info["token"]["validation"]["message"])
        return msg, 401

    msg.append("INFO: Token succesfully decoded. Claims are:")
    msg.append("<pre>" +
               json.dumps(
                   token_info["token"]["claims"],
                   sort_keys=True,
                   indent=4) +
               "</pre>"
               )

    msg.append("INFO: Signing certificate data:")
    msg.append("<pre>" +
               json.dumps(
                   token_info["x509"]["data"],
                   sort_keys=True,
                   indent=4) +
               "</pre>"
               )

    # Check certificate chain
    if token_info["x509"]["validation"]["error"] == 0:
        msg.append("INFO: " + token_info["x509"]["validation"]["message"])
    else:
        msg.append("WARNING: " + token_info["x509"]["validation"]["message"])
        status = 401

    # Check CN
    if token_info["x509"]["data"]["cn"] == token_info["token"]["claims"]["systeminfo"]["hostname"]:
        msg.append("INFO: System hostname matches certificate CN.")
    else:
        msg.append("WARNING: Certificate/Host name mismatch.")
        status = 401

    # Check that this response is for my last request
    try:
        if token_info["token"]["claims"]["requestdata"]["requestId"] == session["requestId"]:
            msg.append("INFO: Token is for the expected request.")
        else:
            msg.append("WARNING: Token is for another request.")
            status = 401

    except Exception:
        msg.append("ERROR: Token format unknown.")
        status = 401

    # Check that this token is issued in the next 10 seconds of the request
    # Not match the device time, because it could be off-time.
    # Use the request session timeof instead.

    if int(time.time()) - session["timeof"] < 10:
        msg.append("INFO: Token is on-time.")
    else:
        msg.append("WARNING: Token wait expired, reload the page.")
        status = 401

    msg.append("DEBUG: JSON API response:")
    msg.append("<pre>" +
               json.dumps(
                   token_info,
                   sort_keys=True,
                   indent=4) +
               "</pre>"
               )

    return msg, status


# Initialization for wsgi and standalone:
cfgfile = "config.json"

config = get_config(cfgfile)
logging.basicConfig(level=config["log_level"])

pem_ca_chain = []
for cert in config["cachain"]:
    pem_ca_chain.append(load_file(cert))
logging.info("Loaded CA certificate chain.")

app.secret_key = config["session_secret"]


if __name__ == '__main__':
    app.run(host=config["listen_ip"],
            port=config["http_port"])
