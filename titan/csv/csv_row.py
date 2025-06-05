class CSVRow:
    def __init__(self, table) -> None:
        self.table = table
        self.row_offset = table.get_column_row_count()

    def get_row_offset(self) -> int:
        return self.row_offset

    def get_value_at(self, column_index: int, index: int):
        return self.table.get_value_at(column_index, self.row_offset + index)

    def get_longest_array_size(self) -> int:
        longest_array_size = 1
        column_count = self.table.get_column_count()

        for i in range(column_count - 1, 0, -1):
            array_size_at = self.table.get_array_size_at(self, i)
            if array_size_at > longest_array_size:
                longest_array_size = array_size_at

        return longest_array_size

    def get_value(self, name: str, index: int):
        column_index = self.table.get_column_index_by_name(name)
        if column_index == -1:
            return ""
        return self.table.get_value_at(column_index, self.row_offset + index)

    def get_clamped_value(self, name: str, index: int) -> str:
        column_index_by_name = self.table.get_column_index_by_name(name)
        if column_index_by_name != -1:
            array_size = self.table.get_array_size_at(self, index)
            if array_size >= 1 and array_size <= index:
                index = array_size - 1
            return self.table.get_value_at(
                column_index_by_name, index + self.row_offset
            )
        return ""

    def get_integer_value(self, name: str, index: int) -> int:
        return self.table.get_integer_value(name, self.row_offset + index)

    def get_clamped_integer_value(self, name: str, index: int) -> int:
        column_index = self.table.get_column_index_by_name(name)
        if column_index == -1:
            return 0
        array_size = self.table.get_array_size_at(self, column_index)
        if array_size >= 1 and array_size <= index:
            index = array_size - 1
        return self.table.get_integer_value_at(column_index, self.row_offset + index)

    def get_boolean_value(self, name: str, index: int) -> bool:
        column_index = self.table.get_column_index_by_name(name)
        if column_index == -1:
            return False
        return self.table.get_boolean_value_at(column_index, self.row_offset + index)

    def get_clamped_boolean_value(self, name: str, index: int) -> bool:
        column_index = self.table.get_column_index_by_name(name)
        if column_index == -1:
            return False
        array_size = self.table.get_array_size_at(self, column_index)
        if array_size >= 1 and array_size <= index:
            index = array_size - 1
        return self.table.get_boolean_value_at(column_index, self.row_offset + index)

    def get_array_size(self, column: str) -> int:
        column_index = self.table.get_column_index_by_name(column)
        if column_index == -1:
            return 0
        return self.table.get_array_size_at(self, column_index)

    def get_table(self):
        return self.table

    def get_name(self):
        return self.table.get_value_at(0, self.row_offset)
