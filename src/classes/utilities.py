# Standard library imports
import base64
import binascii
import datetime
import json
import os
import re
import sys


def encode_base64(value):
    message_bytes = value.encode("utf8")
    base64_bytes = base64.b64encode(message_bytes)
    base64_string = base64_bytes.decode("utf8")
    return base64_string


def decode_base64(value):
    base64_bytes = value.encode("utf8")
    message_bytes = base64.b64decode(base64_bytes)
    message_string = message_bytes.decode("utf8")
    return message_string


def secure_encode_base64(value):
    base64_string = encode_base64(value)
    reversed_base64_string = base64_string[::-1]

    reversed_base64_bytes = reversed_base64_string.encode("utf8")
    hex_bytes = binascii.hexlify(reversed_base64_bytes)
    base64_hex_bytes = base64.b64encode(hex_bytes)
    base64_hex_string = base64_hex_bytes.decode("utf8")
    return base64_hex_string


def secure_decode_base64(value):
    base64_hex_bytes = value.encode("utf8")
    hex_bytes = base64.b64decode(base64_hex_bytes)
    reversed_base64_bytes = binascii.unhexlify(hex_bytes)
    reversed_base64_string = reversed_base64_bytes.decode("utf8")

    base64_string = reversed_base64_string[::-1]
    message_string = decode_base64(base64_string)
    return message_string


def resource_path(relative_path):
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # noinspection PyProtectedMember
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def valid_time(time):
    return (re.match(r"[^0-9:]", time) is None) and \
           (re.match(r"^([0-9]|0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$", time) is not None)


def get_previous_working_date(time=None):
    if time is None:
        time = datetime.datetime.today()
    shift = datetime.timedelta(max(1, (time.weekday() + 6) % 7 - 3))
    return time - shift


def get_js_var(var_name, text, index=0):
    pattern = re.compile('var ' + var_name + ' ?= ?(.*);')
    result = pattern.findall(text)
    if len(result) > 0:
        return result[index]
    else:
        return "{}"


def prettify_json(json_data, debug=False):
    separators = (",", ":")
    if debug:
        return json.dumps(json_data, ensure_ascii=False, separators=separators, indent=4, sort_keys=True)
    else:
        return json.dumps(json_data, ensure_ascii=False, separators=separators)


def get_json_key_by_index(json_data, index):
    return list(json_data.keys())[index]


def json_find_key_by_value(value, json_data):
    key = ""
    for k, v in json_data.items():
        if value.lower() == v.lower():
            key = k
            break
    return key


def json_find_value_by_key(key, json_data):
    value = ""
    for k, v in json_data.items():
        if key.lower() == k.lower():
            value = v
            break
    return value
