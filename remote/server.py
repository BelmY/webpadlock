# -----------------------------------------------------------
# Web Padlock demo server
#
# (C) 2020 Reinoso Guzman, Madrid, Spain
# -----------------------------------------------------------

import json
import time
import logging
from flask import Flask, request, render_template

from libs.config import get_config
from libs.randomstr import get_random_string
from libs.utils import load_file
from libs.jwtchecks import process_token
from libs.stateless import new_auth_session, check_auth_session

global config
global pem_ca_chain

app = Flask(__name__,
            static_url_path='',
            static_folder="web/static",
            template_folder="web/templates")


@app.route('/check')
def check():
    """ Validates a token.
    Method GET.
    URL parameters: token
    Return json object.
    """
    token = request.args.get("token")
    if (token is None):
        return ("Bad Request", 400)
    else:
        token_info = process_token(
            token, pem_ca_chain, config["session_secret"])
        return json.dumps(token_info), 200


@app.route('/start_auth')
def start_auth():
    """
    Creates a new stateless auth session.
    Method: GET
    Parameters: none
    Return: variables to insert in the token request.
    """
    sessionvars = new_auth_session(config["session_secret"])
    return json.dumps(sessionvars), 200


# -------------
# Demo pages. Do not use them in production.
# -------------


@app.route('/')
def home():
    return render_template("index.html",
                           local_server_url=config["local_server_url"])


@app.route('/democheck')
def democheck():
    token = request.args.get("token")
    if (token is None):
        return ("Bad Request", 400)
    else:
        msg, status = webcheck(token)

        fmt_msg = []
        for htmlclass, message in msg:
            fmt_msg.append(
                "<div class='alert alert-{}'>{}</div>".format(htmlclass, message))

        html_message = """
        <div class="row">
            <div class="col-sm">{}</div>
            <div class="col-sm">{}</div>
        </div>
        """.format(fmt_msg[0], fmt_msg[1])

        html_message += """
        <div class="row">
            <div class="col-sm">{}</div>
            <div class="col-sm">{}</div>
        </div>
        """.format(fmt_msg[2], fmt_msg[3])

        html_message += """
        <div class="row">
            <div class="col-sm">{}</div>
            <div class="col-sm">{}</div>
        </div>
        """.format(fmt_msg[4], fmt_msg[5])

        for htmlclass, message in msg[6:]:
            html_message += "<div class='alert alert-{}'>{}</div>".format(
                htmlclass, message)
        return html_message, status


def webcheck(token):
    """
    Compose a status message after the received token.
    This is just an example. The HTML formatting here is nasty.
    You must always use the json api.
    """

    msg = []
    status = 200

    token_info = process_token(token, pem_ca_chain, config["session_secret"])

    # Check token signature
    if token_info["token"]["validation"]["error"] == 0:
        msg.append(["SUCCESS", token_info["token"]["validation"]["message"]])
    else:
        msg.append(["DANGER", token_info["token"]["validation"]["message"]])
        return msg, 401

    msg.append(["SUCCESS", "Token succesfully decoded."])

    # Check certificate chain
    if token_info["x509"]["validation"]["error"] == 0:
        msg.append(["SUCCESS", token_info["x509"]["validation"]["message"]])
    else:
        msg.append(["DANGER", token_info["x509"]["validation"]["message"]])
        status = 401

    # Check CN
    if token_info["x509"]["data"]["cn"] == token_info["token"]["claims"]["systeminfo"]["hostname"]:
        msg.append(["SUCCESS", "System hostname matches certificate CN."])
    else:
        msg.append(["DANGER", "Certificate/Host name mismatch."])
        status = 401

    # Check auth vars present in the token
    if token_info["session"]["present"]:
        msg.append(["SUCCESS", "Valid auth session data."])
    else:
        msg.append(["DANGER", "Invalid auth session data."])
        status = 401

    # Check auth session age (10 seconds max)
    if token_info["session"]["present"]:
        elapsed = token_info["session"]["elapsed"]
        if elapsed < 10:
            msg.append([
                "SUCCESS", "Auth session is recent ({}s).".format(elapsed)
            ])
        else:
            msg.append([
                "WARNING",
                "Auth session is old ({}s). Reload the page.".format(elapsed)
            ])
            status = 401
    else:
        msg.append(["DANGER", "Auth session time data not present."])
        status = 401

    # Dump token claims
    msg.append(["INFO", "Token claims are: <pre>" +
                json.dumps(
                    token_info["token"]["claims"],
                    sort_keys=True,
                    indent=4) +
                "</pre>"])

    msg.append(["INFO", "Signing certificate data: <pre>" +
                json.dumps(
                    token_info["x509"]["data"],
                    sort_keys=True,
                    indent=4) +
                "</pre>"])

    msg.append(["LIGHT", "Raw JSON API response (for DEBUG): <pre>" +
                json.dumps(
                    token_info,
                    sort_keys=True,
                    indent=4) +
                "</pre>"])

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
