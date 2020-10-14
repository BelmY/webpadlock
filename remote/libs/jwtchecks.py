from jwcrypto import jws
from .crypto import verify_pem_chain, validate_token, get_cert_data

# Here you can add all the additional checks you need, based on token.


def process_token(token, pem_ca_chain):
    """
    Make all the token comprobations.
    Input: 
        token: serialized WebPadlock token
        pem_ca_chan: array of PEM trusted certificates
    Output: dictionary, read the documentation.
    """

    # Compose response in case early aborting
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
        return response
    except Exception as e:
        response["token"]["validation"] = {
            "error": 2,
            "message": "Decoding error: {}".format(e)
        }
        return response

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

    return response
