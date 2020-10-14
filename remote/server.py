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
from libs.crypto import verify_pem_chain, validate_token, get_cert_data

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
def jsoncheck_wrap():
    token = request.args.get("token")
    if (token is None):
        return ("Bad Request", 400)
    else:
        return jsoncheck(token)


def jsoncheck(token):
    """
    Validate a token and compose a response in JSON format.
    Always return 200.
    """

    response = {
        "token": {
            "validation": None,
            "claims": None
        },
        "x509": {
            "validation": None,
            "data": None
        }
    }

    # Check token signature
    try:
        pemchain, claims = validate_token(token)
        response["token"]["claims"] = claims
        response["token"]["validation"] = {
            "error": 0,
            "message": "Signature is valid"
        }
    except jws.InvalidJWSSignature:
        response["token"]["validation"] = {
            "error": 1,
            "message": "Invalid signature"
        }
        return json.dumps(response), 200
    except Exception as e:
        response["token"]["validation"] = {
            "error": 2,
            "message": "Decoding error: {}".format(e)
        }
        return json.dumps(response), 200

    # Check certificate chain
    try:
        verify_pem_chain(pemchain, pem_ca_chain)
        response["x509"]["data"] = get_cert_data(pemchain[0])
        response["x509"]["validation"] = {
            "error": 0,
            "message": "Valid x509 certificate"
        }
    except Exception as e:
        response["x509"]["validation"] = {
            "error": 1,
            "message": "Certificate chain verification failed: {}".format(e)
        }

    return json.dumps(response), 200


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
        verify_pem_chain(pemchain, pem_ca_chain)
        msg.append("INFO: Certificate verification OK")
    except Exception as e:
        msg.append("WARNING: Certificate verification failed: {}".format(e))
        status = 401

    certdata = get_cert_data(pemchain[0])
    msg.append("INFO: Signing certificate data is:")
    msg.append("<pre>"+json.dumps(certdata, sort_keys=True, indent=4)+"</pre>")

    # Check hostname
    try:
        certdata = get_cert_data(pemchain[0])

        if certdata["cn"] == claims["systeminfo"]["hostname"]:
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
            msg.append("WARNING: Token wait expired, reload the page.")
            status = 401

    except Exception:
        msg.append("ERROR: Token format unknown.")
        status = 401

    return msg, status


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
