from typing import Dict, List

from .logic_json_node import LogicJSONNode, LogicJSONNodeType


class LogicJSONObject(LogicJSONNode):
    def __init__(self, capacity: int = 0):
        self.m_keys: List[str] = []
        self.m_values: List[LogicJSONNode] = []

    def get(self, key: str) -> LogicJSONNode:
        try:
            idx = self.m_keys.index(key)
            return self.m_values[idx]
        except ValueError:
            return None

    def get_json_boolean(self, key: str):
        node = self.get(key)
        if node and node.get_type() == LogicJSONNodeType.BOOLEAN:
            return node
        print(
            f"LogicJSONObject.get_json_boolean type is {node.get_type() if node else 'None'}, key {key}"
        )
        return None

    def get_json_number(self, key: str):
        node = self.get(key)
        if node and node.get_type() == LogicJSONNodeType.NUMBER:
            return node
        print(
            f"LogicJSONObject.get_json_number type is {node.get_type() if node else 'None'}, key {key}"
        )
        return None

    def get_json_object(self, key: str):
        node = self.get(key)
        if node and node.get_type() == LogicJSONNodeType.OBJECT:
            return node
        print(
            f"LogicJSONObject.get_json_object type is {node.get_type() if node else 'None'}, key {key}"
        )
        return None

    def get_json_string(self, key: str):
        node = self.get(key)
        if node and node.get_type() == LogicJSONNodeType.STRING:
            return node
        print(
            f"LogicJSONObject.get_json_string type is {node.get_type() if node else 'None'}, key {key}"
        )
        return None

    def get_json_array(self, key: str):
        from .logic_json_array import LogicJSONArray

        node = self.get(key)
        if node and node.get_type() == LogicJSONNodeType.ARRAY:
            return node
        print(
            f"LogicJSONObject.get_json_array type is {node.get_type() if node else 'None'}, key {key}"
        )
        return None

    def get_type(self) -> LogicJSONNodeType:
        return LogicJSONNodeType.OBJECT

    def put(self, key: str, item: LogicJSONNode) -> None:
        if key in self.m_keys:
            print(f"LogicJSONObject.put already contains key {key}")
        elif item in self.m_values:
            print(
                f"LogicJSONObject.put already contains the given JSONNode pointer. Key {key}"
            )
        else:
            self.m_keys.append(key)
            self.m_values.append(item)

    def remove(self, key: str) -> None:
        try:
            idx = self.m_keys.index(key)
            self.m_keys.pop(idx)
            self.m_values.pop(idx)
        except ValueError:
            pass

    def get_object_count(self) -> int:
        return len(self.m_values)

    def write_to_string(self, builder: list) -> None:
        builder.append("{")
        for i, key in enumerate(self.m_keys):
            if i > 0:
                builder.append(",")

            from . import LogicJSONParser

            LogicJSONParser.write_string(key, builder)
            builder.append(":")
            self.m_values[i].write_to_string(builder)
        builder.append("}")
