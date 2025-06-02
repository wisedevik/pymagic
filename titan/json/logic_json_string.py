from .logic_json_node import LogicJSONNode, LogicJSONNodeType
from .logic_json_parser import LogicJSONParser


class LogicJSONString(LogicJSONNode):
    def __init__(self, value: str):
        self.m_value = value

    def get_string_value(self) -> str:
        return self.m_value

    def get_type(self) -> LogicJSONNodeType:
        return LogicJSONNodeType.STRING

    def write_to_string(self, builder: list) -> None:
        LogicJSONParser.write_string(self.m_value, builder)
