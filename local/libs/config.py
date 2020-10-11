def get_config():
    """ Read configuration parameters"""
    config = {}
    config["private_key"] = "workstation001-key.pem"
    config["certificate"] = "workstation001-cert.pem"
    config["log_level"] = 10  # logging.DEBUG

    return config


if __name__ == '__main__':
    import json
    print("Configuration dict:")
    print(json.dumps(get_config(), sort_keys=True, indent=4))
