import json
import logging
from jwcrypto import jwt, jwk, jws


from libs.crypto import verify_pem_chain, validate_token
from libs.config import get_config
from libs.utils import load_file
from libs.jwtchecks import check_hostname, check_request_param


config = get_config()
logging.basicConfig(level=config["log_level"])

pemcacert = load_file(config["cacert"])
testtoken = load_file("testtoken.dat")

# Check token signature
try:
    pemchain, claims = validate_token(testtoken)
    logging.info("Decoding token ok")
except (jws.InvalidJWSSignature) as e:
    logging.fatal("Token signature verification failed.")
    exit()
except Exception as e:
    logging.fatal("Decoding token failed: {}".format(e))
    exit()

# Check certificate chain
try:
    verify_pem_chain(pemchain, pemcacert)
    logging.info("Certificate verification OK")
except Exception as e:
    logging.warning("Certificate verification failed.")


# Check hostname
try:
    if (check_hostname(pemchain, claims)):
        logging.info("System hostname matches certificate CN.")
    else:
        logging.warning("Certificate/Host name mismatch.")

except Exception:
    logging.warning("Error matching hostname.")


# Check that this response is for my last request
req_nonce = "f01253ff497eae7fa1555c34a822c2498835c58b"
try:
    if (check_request_param(req_nonce, claims, "nonce")):
        logging.info("Token is for the expected request.")
    else:
        logging.warning("Token is for another request.")

except Exception:
    logging.warning("Token format unknown.")
