from titan.util.logic_array_list import LogicArrayList
from typing import Optional


class CSVColumn:
    def __init__(self, type: int, size: int) -> None:
        self._type = type

        self._string_values_list: LogicArrayList[str] = LogicArrayList[str]()
        self._int_values_list: LogicArrayList[int] = LogicArrayList[int]()
        self._boolean_value_list: LogicArrayList[int] = LogicArrayList[int]()

        match (type):
            case 0:
                self._string_values_list.ensure_capacity(size)
            case 1:
                self._int_values_list.ensure_capacity(size)
            case 2:
                self._boolean_value_list.ensure_capacity(size)

    def add_int_value(self, value: int) -> None:
        self._int_values_list.add(value)

    def get_int_value(self, index: int) -> int:
        result = self._int_values_list[index]
        if result == 0x7FFFFFFF:
            return 0

        return result

    def add_boolean_value(self, value: bool) -> None:
        self._boolean_value_list.add(1 if value else 0)

    def get_boolean_value(self, index: int) -> bool:
        val = self._boolean_value_list[index]
        return val == 1

    def add_string_value(self, value: str) -> None:
        self._string_values_list.add(value)

    def get_string_value(self, index: int) -> str:
        return self._string_values_list[index]

    def get_size(self) -> int:
        match self._type:
            case 0:
                return self._string_values_list.count
            case 1:
                return self._int_values_list.count
            case 2:
                return self._boolean_value_list.count

        return 0

    def get_type(self) -> int:
        return self._type

    def get_array_size(self, start_offset: int, end_offset: int) -> int:
        match self._type:
            case 0:
                if self._string_values_list is None:
                    return 0
                for i in range(end_offset - 1, start_offset - 1, -1):
                    if len(self._string_values_list[i]) > 0:
                        return i - start_offset + 1

            case 1:
                if self._int_values_list is None:
                    return 0
                for i in range(end_offset - 1, start_offset - 1, -1):
                    if self._int_values_list[i] != 0x7FFFFFFF:
                        return i - start_offset + 1

            case 2:
                if self._boolean_value_list is None:
                    return 0
                for i in range(end_offset - 1, start_offset - 1, -1):
                    if self._boolean_value_list[i] != 0x2:
                        return i - start_offset + 1

        return 0

    def set_integer_value(self, value: int, idx: int) -> None:
        self._int_values_list[idx] = value

    def set_boolean_value(self, value: bool, idx: int) -> None:
        self._boolean_value_list[idx] = value

    def set_string_value(self, value: str, idx: int) -> None:
        self._string_values_list[idx] = value

    def add_empty_value(self) -> None:
        match self._type:
            case 0:
                self._string_values_list.add("")
            case 1:
                self._int_values_list.add(0x7FFFFFFF)
            case 2:
                self._boolean_value_list.add(0x2)

    def clone(self) -> "CSVColumn":
        size = self.get_size()
        cloned = CSVColumn(self._type, size)

        match self._type:
            case 0:
                cloned._string_values_list.clear()
                for i in range(size):
                    cloned._string_values_list.add(self._string_values_list[i])

            case 1:
                cloned._int_values_list.clear()
                for i in range(size):
                    cloned._int_values_list.add(self._int_values_list[i])

            case 2:
                cloned._boolean_value_list.clear()
                for i in range(size):
                    cloned._boolean_value_list.add(self._boolean_value_list[i])

        return cloned
