from titan.util.logic_array_list import LogicArrayList

from typing import Optional

class CSVColumn:
    def __init__(self, type: int, size: int) -> None:
        self._type = type

        self._stringValuesList: LogicArrayList[str] = LogicArrayList[str]()
        self._intValuesList: LogicArrayList[int] = LogicArrayList[int]()
        self._booleanValueList: LogicArrayList[int] = LogicArrayList[int]()

        match (type):
            case 0:
                self._stringValuesList.ensure_capacity(size)
            case 1:
                self._intValuesList.ensure_capacity(size)
            case 2:
                self._booleanValueList.ensure_capacity(size)

    def add_int_value(self, value: int) -> None:
        self._intValuesList.add(value)

    def get_int_value(self, index: int) -> int:
        result = self._intValuesList[index]
        if result == 0x7FFFFFFF:
            return 0

        return result

    def add_boolean_value(self, value: bool) -> None:
        self._booleanValueList.add(1 if value else 0)

    def get_boolean_value(self, index: int) -> bool:
        val = self._booleanValueList[index]
        return val == 1

    def add_string_value(self, value: str) -> None:
        self._stringValuesList.add(value)

    def get_string_value(self, index: int) -> str:
        return self._stringValuesList[index]

    def get_size(self) -> int:
        match self._type:
            case 0:
                return self._stringValuesList.count
            case 1:
                return self._intValuesList.count
            case 2:
                return self._booleanValueList.count

        return 0

    def get_type(self) -> int:
        return self._type

    def get_array_size(self, start_offset: int, end_offset: int) -> int:
            match self._type:
                case 0:
                    if self._stringValuesList is None:
                        return 0
                    for i in range(end_offset - 1, start_offset - 1, -1):
                        if len(self._stringValuesList[i]) > 0:
                            return i - start_offset + 1

                case 1:
                    if self._intValuesList is None:
                        return 0
                    for i in range(end_offset - 1, start_offset - 1, -1):
                        if self._intValuesList[i] != 0x7FFFFFFF:
                            return i - start_offset + 1

                case 2:
                    if self._booleanValueList is None:
                        return 0
                    for i in range(end_offset - 1, start_offset - 1, -1):
                        if self._booleanValueList[i] != 0x2:
                            return i - start_offset + 1

            return 0

    def set_integer_value(self, value: int, idx: int) -> None:
        self._intValuesList[idx] = value

    def set_boolean_value(self, value: bool, idx: int) -> None:
        self._booleanValueList[idx] = value

    def set_string_value(self, value: str, idx: int) -> None:
        self._stringValuesList[idx] = value

    def add_empty_value(self) -> None:
        match self._type:
            case 0:
                self._stringValuesList.add("")
            case 1:
                self._intValuesList.add(0x7FFFFFFF)
            case 2:
                self._booleanValueList.add(0x2)

    def clone(self) -> "CSVColumn":
        size = self.get_size()
        cloned = CSVColumn(self._type, size)

        match self._type:
            case 0:
                cloned._stringValuesList.clear()
                for i in range(size):
                    cloned._stringValuesList.add(self._stringValuesList[i])

            case 1:
                cloned._intValuesList.clear()
                for i in range(size):
                    cloned._intValuesList.add(self._intValuesList[i])

            case 2:
                cloned._booleanValueList.clear()
                for i in range(size):
                    cloned._booleanValueList.add(self._booleanValueList[i])

        return cloned
