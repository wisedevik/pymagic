import json


class Config:
    _data = None

    @classmethod
    def load(cls, filename="config.json"):
        with open(filename, "r") as f:
            cls._data = json.load(f)

    @classmethod
    def get(cls, key, default=None):
        if cls._data is None:
            raise RuntimeError("Config is not loaded yet")
        return cls._data.get(key, default)

    @classmethod
    def __getitem__(cls, key):
        if cls._data is None:
            raise RuntimeError("Config is not loaded yet")
        return cls._data[key]
