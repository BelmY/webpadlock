from jwcrypto import jwk, jwt
from jwcrypto.common import json_encode
import logging


def load_private(file):
    """Load private key in PEM format from first param.
    Return a JWK object."""
    with open(file, "rb") as pemfile:
        key = jwk.JWK.from_pem(pemfile.read())

    logging.info('Loaded private key from {}'.format(file))
    return key


def load_public(file):
    """Load certificate in PEM format from first param. 
    Return the stripped data (no BEGIN/END lines)."""
    with open(file, "r") as pemfile:
        cert_content = pemfile.read()
        cert_stripped = "".join(
            [line for line in cert_content.splitlines() if "CERTIFICATE" not in line])

    logging.info('Loaded certificate from {}'.format(file))
    return cert_stripped


def jwt_header(cert):
    """Return a dict with the JWT header.
    Use global var: cert."""
    header = {}
    header["alg"] = "RS256"
    header["x5c"] = cert
    return header


def create_jwt(key, cert, claims):
    """Return a serialized JWT with indicated claims. Params:
    key: JWK with RSA private key.
    cert: RSA certificate data (stripped)
    claims: dictionary with the claims"""

    token = jwt.JWT(header=json_encode(jwt_header(cert)),
                    claims=json_encode(claims))
    token.make_signed_token(key)
    return token.serialize()


def get_systeminfo():
    """Return a dictionary with information about the host system"""
    info = {}
    info["hostname"] = "workstation001"
    return info


def get_metadata():
    """Return metadata about the response"""
    info = {}
    info["version"] = {}
    info["version"]["mayor"] = "1"
    info["version"]["minor"] = "0"
    return info


def init():
    """Set config, initialize the server"""
    config = {}
    config["private_key"] = "workstation001-key.pem"
    config["certificate"] = "workstation001-cert.pem"
    config["log_level"] = 10  # logging.DEBUG

    logging.basicConfig(level=config["log_level"])

    key = load_private(config["private_key"])
    cert = load_public(config["certificate"])

    origin_data = {}
    origin_data["nonce"] = "f01253ff497eae7fa1555c34a822c2498835c58b"

    claims = {}
    claims["systeminfo"] = get_systeminfo()
    claims["metadata"] = get_metadata()
    claims["origin"] = origin_data

    token = create_jwt(key, cert, claims)
    print(token)


init()
