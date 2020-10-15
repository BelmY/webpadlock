import sys
import json
import logging
from jwcrypto import jws

from libs.config import get_config
from libs.utils import load_file
from libs.jwtchecks import process_token
from libs.stateless import check_auth_session

cfgfile = "config.json"


if len(sys.argv) < 2:
    print("Web Padlock. Command line interface for testing purposes.")
    print("Usage: {} tokenfile".format(sys.argv[0]))
    exit()


try:
    testtoken = load_file(sys.argv[1])
    print(testtoken)
except Exception as e:
    logging.fatal("Error reading token: {}".format(e))
    exit()


config = get_config(cfgfile)
logging.basicConfig(level=config["log_level"])

pem_ca_chain = []
for cert in config["cachain"]:
    pem_ca_chain.append(load_file(cert))

token_info = process_token(testtoken, pem_ca_chain, config["session_secret"])

# Check token signature
if token_info["token"]["validation"]["error"] == 0:
    logging.info(token_info["token"]["validation"]["message"])
else:
    logging.critical(token_info["token"]["validation"]["message"])

print("")
print("Certificate data:")
print(json.dumps(token_info["x509"]["data"], sort_keys=True, indent=4))

# Check certificate chain
if token_info["x509"]["validation"]["error"] == 0:
    logging.info(token_info["x509"]["validation"]["message"])
else:
    logging.warning(token_info["x509"]["validation"]["message"])


if token_info["x509"]["data"]["cn"] == token_info["token"]["claims"]["systeminfo"]["hostname"]:
    logging.info("System hostname matches certificate CN.")
else:
    logging.warning("Certificate/Host name mismatch.")

# Check session data
    # Check auth session age (10 seconds max)
    if token_info["session"]["present"]:
        logging.info(
            "Auth session started {} seconds ago.".format(token_info["session"]["elapsed"]))
    else:
        logging.warning("Auth session time data not present or invalid.")

print("")
print("Token claims:")
print(json.dumps(token_info["token"]["claims"], sort_keys=True, indent=4))
