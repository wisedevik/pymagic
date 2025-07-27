from titan.csv.csv_row import CSVRow
from titan.csv.csv_table import CSVTable
from titan.debug.debugger import Debugger


class LogicStringTable:
    s_instance = None

    def __init__(self, table: CSVTable):
        self.table: CSVTable = table
        self.strings: dict[str, CSVRow] = dict()

        if table.get_row_count() >= 1:
            for i in range(table.get_row_count()):
                row_at = table.get_row_at(i)
                tid_value = row_at.get_value_at(0, 0)

                if tid_value not in self.strings:
                    self.strings[tid_value] = row_at
                else:
                    Debugger.warning(f"duplicate TID in {tid_value}")

    @staticmethod
    def create_instance(table: CSVTable):
        if LogicStringTable.s_instance is None:
            LogicStringTable.s_instance = LogicStringTable(table)
        else:
            Debugger.warning("LogicStringTable instance already created")

    def get_language_code(self, idx):
        return self.table.get_column_name(idx)

    @staticmethod
    def get_instance():
        return LogicStringTable.s_instance

    def get_string(self, tid, column_index):
        row = self.strings.get(tid)
        if row is None:
            Debugger.warning(f"Can't find TID: {tid}")
            return None

        value_at = row.get_value_at(column_index, 0)
        return value_at
