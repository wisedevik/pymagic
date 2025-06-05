from logic.data.core.logic_data_type import LogicDataType


class LogicDataTableResource:
    def __init__(self, file_name: str, table_index: LogicDataType, type: int) -> None:
        self.file_name = file_name
        self.table_index = table_index
        self.type = type

    def get_file_name(self) -> str:
        return self.file_name

    def get_table_index(self) -> LogicDataType:
        return self.table_index

    def get_type(self) -> int:
        return self.type
