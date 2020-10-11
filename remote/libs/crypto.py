import json
import logging
from OpenSSL import crypto
from jwcrypto import jwt, jwk, jws
from cryptography import x509
from cryptography.x509.oid import NameOID


def jwt_pemchain(token):
    """Extract signing x.509 certificate. A better method must exists.
    jwt: a serialized jwt with x5c array.
    Return an array of PEM certificates."""

    pemchain = []

    sign = jws.JWS()
    sign.deserialize(token)

    for stripped_cert in sign.jose_header["x5c"]:
        cert = \
            "-----BEGIN CERTIFICATE-----\n" + \
            stripped_cert + \
            "\n-----END CERTIFICATE-----"

        pemchain.append(str.encode(cert))

    return pemchain


def validate_token(jwt_str, pem_data):
    """ Check token signature using the first certificate as key.
    You also MUST validate that certificate by another way.

    jwt_str: serialized jwt data
    pem_data: certificate in PEM format
    Return a dict with token claims"""

    key = jwk.JWK.from_pem(pem_data)
    token = jwt.JWT(jwt=jwt_str, key=key)
    return json.loads(token.claims)


def get_cert_cn(pem_data):
    """ Return the CN of the certificate given in pem_data. """

    cert = x509.load_pem_x509_certificate(pem_data)
    cn = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    return cn


def verify_certificate_using_other(pem_incognito, pem_trusted):
    store = crypto.X509Store()

    # Add trusted cert
    trusted = crypto.load_certificate(crypto.FILETYPE_PEM, pem_trusted)
    store.add_cert(trusted)

    # Add incognito cert to context
    incognito = crypto.load_certificate(crypto.FILETYPE_PEM, pem_incognito)
    store_ctx = crypto.X509StoreContext(store, incognito)

    try:
        store_ctx.verify_certificate()
        return True

    except Exception as e:
        logging.warning(e)
        return False
