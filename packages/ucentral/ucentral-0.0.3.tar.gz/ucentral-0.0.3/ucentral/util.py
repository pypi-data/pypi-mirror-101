def duck(value):
    if isinstance(value, str):
        if value.isdigit():
            return int(value)
        elif value.isdecimal():
            return float(value)
    return value


def merge(src, dest):
    for key, value in src.items():
        if isinstance(value, dict):
            node = dest.setdefault(key, {})
            merge(value, node)
        else:
            dest[key] = value

    return dest
