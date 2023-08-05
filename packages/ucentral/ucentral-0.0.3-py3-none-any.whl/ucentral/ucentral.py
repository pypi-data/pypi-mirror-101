import json

from dotty_dict import dotty
from jsonschema import ValidationError, validate

from ucentral.util import duck, merge


class Ucentral:
    def __init__(self):
        self.config = dotty({})
        self.schema = {}
        self.last_load_path = None
        self.last_schema_path = None
        self.last_write_path = None

    def apply_if_valid(self, tmp_config, ret=True):
        try:
            validate(instance=tmp_config.to_dict(), schema=self.schema)
            self.config.update(tmp_config)
            return ret
        except ValidationError as e:
            return e

    def add(self, path):
        tmp_config = dotty()
        tmp_config.update(self.config)

        tmp_config.setdefault(path, [])
        tmp_config[path].append({})
        elements = len(tmp_config[path]) - 1

        return self.apply_if_valid(tmp_config, f"{path}.{elements}")

    def add_list(self, path, value):
        tmp_config = dotty()
        tmp_config.update(self.config)

        tmp_config.setdefault(path, [])
        tmp_config[path].append(duck(value))

        return self.apply_if_valid(tmp_config)

    def del_list(self, path, value):
        tmp_config = dotty()
        tmp_config.update(self.config)

        if isinstance(tmp_config[path], list):
            tmp_config[path].remove(duck(value))
        else:
            return f"{path} is not a list"

        return self.apply_if_valid(tmp_config)

    def get(self, path):
        return self.config.get(path)

    def set(self, path, value):
        tmp_config = dotty()
        tmp_config.update(self.config)

        tmp_config[path] = duck(value)

        return self.apply_if_valid(tmp_config)

    def show(self):
        return self.config.to_json()

    def load(self, filename: str):
        if not filename:
            filename = self.last_load_path

        tmp_config = json.load(open(filename))

        return self.apply_if_valid(tmp_config)

    def schema_load(self, filename: str):
        if not filename:
            filename = self.last_schema_path
        self.schema = json.load(open(filename))

        self.last_schema_path = filename
        return f"Schema loaded from {filename}"

    def write(self, filename: str = None):
        if not filename:
            filename = self.last_write_path

        json.dump(self.config.to_dict(), open(filename, "w"), sort_keys=True, indent=4)

        self.last_write_path = filename

        return f"Config written to {filename}"

    def merge(self, obj):
        tmp_config = dotty()
        tmp_config.update(self.config)

        merge(obj, tmp_config)

        return self.apply_if_valid(tmp_config)
