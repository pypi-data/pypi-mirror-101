import json


def duck(value):
    if isinstance(value, str):
        if value.isdecimal():
            return int(value)

        try:
            return float(value)
        except ValueError:
            pass
    return value


def merge(src, dest):
    for key, value in src.items():
        if isinstance(value, dict):
            node = dest.setdefault(key, {})
            merge(value, node)
        else:
            dest[key] = value

    return dest


def pretty(data: dict):
    return json.dumps(data, indent=4, sort_keys=True)
