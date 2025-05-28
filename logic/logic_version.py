from dataclasses import dataclass

from config import Config


class LogicVersion:
    @classmethod
    def major_version(cls):
        return Config.get("majorVersion")

    @classmethod
    def build(cls):
        return Config.get("build")

    @classmethod
    def content_version(cls):
        return Config.get("contentVersion")
