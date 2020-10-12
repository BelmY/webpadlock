import json
import logging
from OpenSSL import crypto
from jwcrypto import jwt, jwk, jws


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


def validate_token(jwt_str):
    """ Check token signature using the first certificate as key.
    You also MUST validate that certificate by another way.

    jwt_str: serialized jwt data
    Return an array of PEM certs, and a dict with token claims
    Exception on failure. """

    pemchain = jwt_pemchain(jwt_str)

    key = jwk.JWK.from_pem(pemchain[0])
    token = jwt.JWT(jwt=jwt_str, key=key)
    return pemchain, json.loads(token.claims)


def verify_certificate_using_other(pem_incognito, pem_trusted):
    """ Verify one certificate in the context of another trusted. 
    Return true if Ok, Exception in failure """
    store = crypto.X509Store()

    # Add trusted cert
    trusted = crypto.load_certificate(crypto.FILETYPE_PEM, pem_trusted)
    store.add_cert(trusted)

    # Add incognito cert to context
    incognito = crypto.load_certificate(crypto.FILETYPE_PEM, pem_incognito)
    store_ctx = crypto.X509StoreContext(store, incognito)

    store_ctx.verify_certificate()
    return True


def verify_pem_chain(pemchain, pemca):
    """ Verify the certificate chain. 
    NOTE: Only two at the moment. 
    Return true if Ok, Exception in failure. """
    return verify_certificate_using_other(pemchain[0], pemca)
