from .logic_json_node import LogicJSONNode, LogicJSONNodeType


class LogicJSONNumber(LogicJSONNode):
    def __init__(self, value: int = 0):
        self.m_value = value

    def get_int_value(self) -> int:
        return self.m_value

    def set_int_value(self, value: int) -> None:
        self.m_value = value

    def get_type(self) -> LogicJSONNodeType:
        return LogicJSONNodeType.NUMBER

    def write_to_string(self, builder: list) -> None:
        builder.append(str(self.m_value))
