from typing import Optional

from titan.csv.csv_column import CSVColumn
from titan.csv.csv_row import CSVRow
from titan.debug.debugger import Debugger
from titan.util.logic_array_list import LogicArrayList


class CSVTable:
    def __init__(self, node, size: int) -> None:
        self._columnNameList: LogicArrayList[str] = LogicArrayList[str]()
        self._columnList: LogicArrayList[CSVColumn] = LogicArrayList[CSVColumn]()
        self._rowList: LogicArrayList[CSVRow] = LogicArrayList[CSVRow]()

        self._size = size
        self._node = node

    def add_column(self, name: str) -> None:
        self._columnNameList.add(name)

    @staticmethod
    def str_to_bool(value: str) -> tuple[bool, bool]:
        if isinstance(value, str):
            val_lower = value.strip().lower()
            if val_lower in ["true"]:
                return True, True
            elif val_lower in ["false"]:
                return True, False
        return False, False

    def add_and_convert_value(self, value: str, index: int) -> None:
        column = self._columnList[index]

        if value is not None and value != "":
            match column.get_type():
                case 0:
                    column.add_string_value(value)
                case 1:
                    column.add_int_value(int(value))
                case 2:
                    success, boolean_value = CSVTable.str_to_bool(value)
                    if success:
                        column.add_boolean_value(bool(value))
                    else:
                        Debugger.warning(
                            f"CSVTable.add_and_convert_value invalid value '{value}' in Boolean column '{self._columnNameList[index]}', {self.get_file_name()}"
                        )

                        column.add_boolean_value(False)
        else:
            column.add_empty_value()

    def get_file_name(self) -> str:
        return self._node.get_name()

    def get_column_name(self, idx: int) -> str:
        return self._columnNameList[idx]

    def add_column_type(self, type: int) -> None:
        self._columnList.add(CSVColumn(type, self._size))

    def get_column_count(self):
        return self._columnList.count

    def get_value_at(self, column_index: int, index: int) -> str:
        if column_index >= 0:
            return self._columnList[column_index].get_string_value(index)

        return ""

    def get_value(self, name: str, index: int) -> str:
        return self.get_value_at(self._columnNameList.index_of(name), index)

    def get_column_index_by_name(self, name: str) -> int:
        return self._columnNameList.index_of(name)

    def get_integer_value_at(self, column_index: int, index: int) -> int:
        if column_index >= 0:
            return self._columnList[column_index].get_int_value(index)

        return 0

    def get_integer_value(self, name: str, index: int) -> int:
        return self.get_integer_value_at(self._columnNameList.index_of(name), index)

    def get_boolean_value_at(self, column_index: int, index: int) -> bool:
        if column_index >= 0:
            return self._columnList[column_index].get_boolean_value(index)

        return False

    def get_boolean_value(self, name: str, index: int) -> bool:
        return self.get_boolean_value_at(self._columnNameList.index_of(name), index)

    def get_row_at(self, index: int) -> CSVRow:
        return self._rowList[index]

    def add_row(self, row: CSVRow) -> None:
        self._rowList.add(row)

    def get_column_row_count(self) -> int:
        return self._columnList[0].get_size()

    def get_row_count_of_CSVRow(self, row: CSVRow) -> int:
        return -1

    def get_row_count(self) -> int:
        return self._rowList.count

    def get_array_size_at(self, row: CSVRow, index: int):
        if self._rowList.count > 0:
            rowIndex = self._rowList.index_of(row)

            if rowIndex != -1:
                column = self._columnList[index]
                return column.get_array_size(
                    self._rowList[rowIndex].get_row_offset(),
                    (
                        column.get_size()
                        if rowIndex + 1 >= self._rowList.count
                        else self._rowList[rowIndex + 1].get_row_offset()
                    ),
                )
        return 0

    def create_row(self) -> None:
        self._rowList.add(CSVRow(self))

    def column_names_loaded(self) -> None:
        self._columnList.ensure_capacity(self._columnNameList.count)

    def validate_column_types(self) -> None:
        if self._columnNameList.count != self._columnList.count:
            Debugger.warning(
                f"Column name count {self._columnNameList.count}, column type count {self._columnList.count}, file {self.get_file_name()}"
            )
