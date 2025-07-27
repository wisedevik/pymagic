from typing import List

from . import LogicJSONNumber
from . import LogicJSONString
from . import LogicJSONNode, LogicJSONNodeType
from . import LogicJSONBoolean


class LogicJSONArray(LogicJSONNode):
    def __init__(self, capacity: int = 0):
        self.m_items: List[LogicJSONNode] = []

    def get(self, idx: int) -> LogicJSONNode:
        return self.m_items[idx]

    def add(self, item: LogicJSONNode) -> None:
        self.m_items.append(item)

    def get_json_array(self, index: int):
        node = self.m_items[index]
        if node.get_type() != LogicJSONNodeType.ARRAY:
            print(
                f"LogicJSONObject.get_json_array wrong type {node.get_type()}, index {index}"
            )
            return None
        return node

    def get_json_boolean(self, index: int) -> LogicJSONBoolean:
        node = self.m_items[index]
        if node.get_type() != LogicJSONNodeType.BOOLEAN:
            print(
                f"LogicJSONObject.get_json_boolean wrong type {node.get_type()}, index {index}"
            )
            return None
        return node

    def get_json_number(self, index: int) -> LogicJSONNumber:
        node = self.m_items[index]
        if node.get_type() != LogicJSONNodeType.NUMBER:
            print(
                f"LogicJSONObject.get_json_number wrong type {node.get_type()}, index {index}"
            )
            return None
        return node

    def get_json_object(self, index: int):
        node = self.m_items[index]
        if node.get_type() != LogicJSONNodeType.OBJECT:
            print(
                f"LogicJSONObject.get_json_object wrong type {node.get_type()}, index {index}"
            )
            return None
        return node

    def get_json_string(self, index: int) -> LogicJSONString:
        node = self.m_items[index]
        if node.get_type() != LogicJSONNodeType.STRING:
            print(
                f"LogicJSONObject.get_json_string wrong type {node.get_type()}, index {index}"
            )
            return None
        return node

    def size(self) -> int:
        return len(self.m_items)

    def get_type(self) -> LogicJSONNodeType:
        return LogicJSONNodeType.ARRAY

    def write_to_string(self, builder: list) -> None:
        builder.append("[")
        for i, item in enumerate(self.m_items):
            if i > 0:
                builder.append(",")
            item.write_to_string(builder)
        builder.append("]")
