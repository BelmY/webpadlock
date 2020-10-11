def get_config():
    """ Read configuration parameters"""
    config = {}
    config["cacert"] = "workstation001-cert.pem"
    config["log_level"] = 10  # logging.DEBUG
    config["http_port"] = 8080
    config["listen_ip"] = "0.0.0.0"

    return config


if __name__ == '__main__':
    import json
    print("Configuration dict:")
    print(json.dumps(get_config(), sort_keys=True, indent=4))
