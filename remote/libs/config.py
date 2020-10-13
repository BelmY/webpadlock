def get_config():
    """ Read configuration parameters"""
    config = {}
    config["cachain"] = ["intermediate.cert.pem", "ca.cert.pem"]
    config["log_level"] = 10  # logging.DEBUG
    config["http_port"] = 10000
    config["listen_ip"] = "0.0.0.0"
    config["session_secret"] = "webpadlock"
    config["local_server_url"] = "http://127.0.0.1:3000/deviceinfo"

    return config


if __name__ == '__main__':
    import json
    print("Configuration dict:")
    print(json.dumps(get_config(), sort_keys=True, indent=4))
