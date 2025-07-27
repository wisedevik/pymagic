from typing import Dict, Any, TypeVar
import toml

from .section import ConfigSection

T = TypeVar("T")


class ConfigurationMeta(type):
    _data: Dict[str, Any] = {}

    def __getattr__(cls, name: str) -> Any:
        value = cls._data[name]
        if isinstance(value, dict):
            return ConfigSection(value)
        return value


class Configuration(metaclass=ConfigurationMeta):
    @classmethod
    def load(cls, path: str = "config.toml") -> None:
        with open(path) as f:
            cls._data = toml.load(f)
