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


def load_cert(file):
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
    cert: array of stripped certificate chain. 
    The first is always the one used for signing."""
    header = {}
    header["alg"] = "RS256"
    header["x5c"] = cert
    return header


def create_jwt(key, cert, systeminfo, metadata, requestdata):
    """Return a serialized webpadlock JWT with indicated claims.
    key: JWK with RSA private key.
    cert: RSA certificate data (stripped)
    systeminfo: Claim "systeminfo" (os version, hostname, etc)
    metadata: Claim "metadata" (webpadlock version, etc)
    requestdata: Claim "requestdata" (copied form the request)
    """

    claims = {}
    claims["systeminfo"] = systeminfo
    claims["metadata"] = metadata
    claims["requestdata"] = requestdata

    logging.debug("Claims:{}".format(json_encode(claims)))

    token = jwt.JWT(header=json_encode(jwt_header([cert])),
                    claims=json_encode(claims))

    token.make_signed_token(key)

    return token.serialize()
