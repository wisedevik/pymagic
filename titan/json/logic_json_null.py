from .logic_json_node import LogicJSONNode, LogicJSONNodeType


class LogicJSONNull(LogicJSONNode):
    def get_type(self) -> LogicJSONNodeType:
        return LogicJSONNodeType.NULL

    def write_to_string(self, builder: list) -> None:
        builder.append("null")
