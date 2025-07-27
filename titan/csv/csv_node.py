from ast import Not
from titan.csv.csv_table import CSVTable
from titan.debug.debugger import Debugger
from titan.util.logic_array_list import LogicArrayList


class CSVNode:
    def __init__(self, lines: list[str], file_name: str):
        self.name = file_name
        self.table: CSVTable | None = None
        self.load(lines)

    def load(self, lines: list[str]) -> None:
        self.table = CSVTable(self, len(lines))

        if len(lines) >= 2:
            column_names = self.parse_line(lines[0])
            column_types = self.parse_line(lines[1])

            for name in column_names:
                self.table.add_column(name)

            for i, raw_type_str in enumerate(column_types):
                column_type = -1
                type_str = raw_type_str.strip()

                if type_str:
                    lowered = type_str.lower()
                    if lowered == "string":
                        column_type = 0
                    elif lowered == "int":
                        column_type = 1
                    elif lowered == "boolean":
                        column_type = 2
                    else:
                        Debugger.error(
                            f"Invalid column type '{type_str}', column name {column_names[i]}, file {self.name}. Expecting: int/string/boolean."
                        )

                self.table.add_column_type(column_type)

            self.table.validate_column_types()

            for i in range(2, len(lines)):
                values = self.parse_line(lines[i])

                if values.count > 0 and values[0]:
                    self.table.create_row()

                    for j, val in enumerate(values):
                        self.table.add_and_convert_value(val, j)

    def parse_line(self, line: str) -> LogicArrayList[str]:
        line = line.rstrip("\n")
        in_quote = False
        read_field = ""
        fields = LogicArrayList[str]()

        i = 0
        while i < len(line):
            char = line[i]
            if char == '"':
                if in_quote:
                    if i + 1 < len(line) and line[i + 1] == '"':
                        read_field += '"'
                        i += 1
                    else:
                        in_quote = False
                else:
                    in_quote = True
            elif char == "," and not in_quote:
                fields.add(read_field)
                read_field = ""
            else:
                read_field += char
            i += 1

        fields.add(read_field)
        return fields

    def set_name(self, name: str) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name

    def get_table(self) -> CSVTable:
        assert self.table is not None
        return self.table
