import json
import sys


def get_config(cfgfile):
    """ Read configuration parameters"""
    with open(cfgfile) as json_file:
        data = json.load(json_file)
    return data


if __name__ == '__main__':
    import json

    if len(sys.argv) < 2:
        cfgfile = "../config.json"
    else:
        cfgfile = sys.argv[1]

    print("Configuration dict:")
    print(json.dumps(get_config(cfgfile), sort_keys=True, indent=4))
