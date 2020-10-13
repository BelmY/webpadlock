import random
import string


def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_metadata():
    """Metadata to add in every response"""
    info = {}
    info["version"] = {}
    info["version"]["mayor"] = "1"
    info["version"]["minor"] = "0"
    info["name"] = "Web Padlock"
    info["tokenid"] = get_random_string(40)

    return info


if __name__ == '__main__':
    import json
    print("Metadata claim:")
    print(json.dumps(get_metadata(), sort_keys=True, indent=4))
