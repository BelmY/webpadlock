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
from jwcrypto import jws

from libs.config import get_config
from libs.randomstr import get_random_string
from libs.utils import load_file
from libs.crypto import verify_pem_chain, validate_token
from libs.jwtchecks import check_hostname, check_request_param

global config
global pemcacert


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
        html_message = "<p>"
        html_message += "</p>\n<p>".join(msg)
        html_message += "</p>\n"
        return html_message, status


def webcheck(token):
    """
    Compose a status message after the received token.
    This is only an example. Your actual check routine will be different.
    """
    msg = []
    status = 200

    # Check token signature
    try:
        pemchain, claims = validate_token(token)
        msg.append("INFO: Token integrity OK")
    except (jws.InvalidJWSSignature) as e:
        msg.append("FATAL: Token signature verification failed.")
        return msg, 401
    except Exception as e:
        msg.append("FATAL: Decoding token failed: {}\n".format(e))
        return msg, 401

    msg.append("INFO: Token succesfully decoded. Claims are:")
    msg.append("<pre>"+json.dumps(claims, sort_keys=True, indent=4)+"</pre>")

    # Check certificate chain
    try:
        verify_pem_chain(pemchain, pemcacert)
        msg.append("INFO: Certificate verification OK")
    except Exception as e:
        msg.append("WARNING: Certificate verification failed: {}".format(e))
        status = 401

    # Check hostname
    try:
        if check_hostname(pemchain, claims):
            msg.append("INFO: System hostname matches certificate CN.")
        else:
            msg.append("WARNING: Certificate/Host name mismatch.")
            status = 401

    except Exception:
        msg.append("ERROR: Error matching hostname.")
        status = 401

    # Check that this response is for my last request
    try:
        if claims["requestdata"]["requestId"] == session["requestId"]:
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
        # Check that this response is for my last request
    # Check that this response is for my last request
    try:
        if int(time.time()) - session["timeof"] < 10:
            msg.append("INFO: Token is on-time.")
        else:
            msg.append("WARNING: Token is delayed, reload the page.")
            status = 401

    except Exception:
        msg.append("ERROR: Token format unknown.")
        status = 401

    return msg, status


if __name__ == '__main__':

    config = get_config()
    logging.basicConfig(level=config["log_level"])

    pemcacert = load_file(config["cacert"])
    logging.info("Loaded CA certificate from {}.".format(config["cacert"]))

    app.secret_key = config["session_secret"]
    app.run(host=config["listen_ip"],
            port=config["http_port"])
