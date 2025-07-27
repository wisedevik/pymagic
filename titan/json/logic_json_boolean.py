from . import LogicJSONNode, LogicJSONNodeType


class LogicJSONBoolean(LogicJSONNode):
    def __init__(self, value: bool):
        self.m_value = value

    def is_true(self) -> bool:
        return self.m_value

    def get_type(self) -> LogicJSONNodeType:
        return LogicJSONNodeType.BOOLEAN

    def write_to_string(self, builder: list) -> None:
        builder.append("true" if self.m_value else "false")
