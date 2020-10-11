import json
import logging
from jwcrypto import jwt, jwk, jws


from libs.crypto import jwt_pemchain, \
    verify_certificate_using_other, \
    validate_token, \
    get_cert_cn
from libs.config import get_config


def load_file(file):
    with open(file, "r") as fileh:
        return fileh.read()


config = get_config()
logging.basicConfig(level=config["log_level"])

testtoken = load_file("testtoken.dat")
pemchain = jwt_pemchain(testtoken)

# Check certificate chain
pemcacert = load_file(config["cacert"])

if (verify_certificate_using_other(pemchain[0], pemcacert)):
    logging.info("Certificate verification OK")
else:
    logging.warning("Certificate verification failed")


# Check token signature
claims = validate_token(testtoken, pemchain[0])


# Check hostname
cert_cn = get_cert_cn(pemchain[0])
hostname = claims["systeminfo"]["hostname"]

if (cert_cn == hostname):
    logging.info("System hostname matches certificate CN.")
else:
    logging.warning("Host mismatch. Hostname is {}, but certificate is for {}.".format(
        hostname,
        cert_cn
    ))

# Check that this response is for my last request
request_id = claims["requestdata"]["nonce"]

print("Request Id is {}.".format(request_id))
