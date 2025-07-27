from typing import Optional

from titan.csv.csv_column import CSVColumn
from titan.csv.csv_row import CSVRow
from titan.debug.debugger import Debugger
from titan.util.logic_array_list import LogicArrayList


class CSVTable:
    def __init__(self, node, size: int) -> None:
        self.column_name_list: LogicArrayList[str] = LogicArrayList[str]()
        self.column_list: LogicArrayList[CSVColumn] = LogicArrayList[CSVColumn]()
        self.row_list: LogicArrayList[CSVRow] = LogicArrayList[CSVRow]()

        self.size = size
        self.node = node

    def add_column(self, name: str) -> None:
        self.column_name_list.add(name)

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
        column = self.column_list[index]

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
                            f"CSVTable.add_and_convert_value invalid value '{value}' "
                            f"in Boolean column '{self.column_name_list[index]}', "
                            f"{self.get_file_name()}"
                        )
                        column.add_boolean_value(False)
        else:
            column.add_empty_value()

    def get_file_name(self) -> str:
        return self.node.get_name()

    def get_column_name(self, idx: int) -> str:
        return self.column_name_list[idx]

    def add_column_type(self, type: int) -> None:
        self.column_list.add(CSVColumn(type, self.size))

    def get_column_count(self):
        return self.column_list.count

    def get_value_at(self, column_index: int, index: int) -> str:
        if column_index >= 0:
            return self.column_list[column_index].get_string_value(index)
        return ""

    def get_value(self, name: str, index: int) -> str:
        return self.get_value_at(self.column_name_list.index_of(name), index)

    def get_column_index_by_name(self, name: str) -> int:
        return self.column_name_list.index_of(name)

    def get_integer_value_at(self, column_index: int, index: int) -> int:
        if column_index >= 0:
            return self.column_list[column_index].get_int_value(index)
        return 0

    def get_integer_value(self, name: str, index: int) -> int:
        return self.get_integer_value_at(self.column_name_list.index_of(name), index)

    def get_boolean_value_at(self, column_index: int, index: int) -> bool:
        if column_index >= 0:
            return self.column_list[column_index].get_boolean_value(index)
        return False

    def get_boolean_value(self, name: str, index: int) -> bool:
        return self.get_boolean_value_at(self.column_name_list.index_of(name), index)

    def get_row_at(self, index: int) -> CSVRow:
        return self.row_list[index]

    def add_row(self, row: CSVRow) -> None:
        self.row_list.add(row)

    def get_column_row_count(self) -> int:
        return self.column_list[0].get_size()

    def get_row_count_of_csv_row(self, row: CSVRow) -> int:
        return -1

    def get_row_count(self) -> int:
        return self.row_list.count

    def get_array_size_at(self, row: CSVRow, index: int):
        if self.row_list.count > 0:
            row_index = self.row_list.index_of(row)

            if row_index != -1:
                column = self.column_list[index]
                return column.get_array_size(
                    self.row_list[row_index].get_row_offset(),
                    (
                        column.get_size()
                        if row_index + 1 >= self.row_list.count
                        else self.row_list[row_index + 1].get_row_offset()
                    ),
                )
        return 0

    def create_row(self) -> None:
        self.row_list.add(CSVRow(self))

    def column_names_loaded(self) -> None:
        self.column_list.ensure_capacity(self.column_name_list.count)

    def validate_column_types(self) -> None:
        if self.column_name_list.count != self.column_list.count:
            Debugger.warning(
                f"Column name count {self.column_name_list.count}, "
                f"column type count {self.column_list.count}, "
                f"file {self.get_file_name()}"
            )
