from enum import Enum


class LogicJSONNodeType(Enum):
    ARRAY = 1
    OBJECT = 2
    NUMBER = 3
    STRING = 4
    BOOLEAN = 5
    NULL = 6


class LogicJSONNode:
    def get_type(self) -> LogicJSONNodeType:
        raise NotImplementedError()

    def write_to_string(self, builder: list) -> None:
        raise NotImplementedError()
