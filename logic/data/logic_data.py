from logic.data.global_id import GlobalID
from logic.data.logic_data_type import LogicDataType
from titan.csv.csv_row import CSVRow


class LogicData:
    def __init__(self, row: CSVRow, table):
        self._row = row
        self._table = table
        self._iconSWF = ""
        self._iconExportName = ""
        self._tid = ""
        self._infoTID = ""
        self._globalId = GlobalID.create_global_ID(
            int(table.get_table_index()) + 1, table.get_item_count()
        )

    def create_references(self):
        self._iconSWF = self._row.get_value("IconSWF", 0)
        self._iconExportName = self._row.get_value("IconExportName", 0)
        self._tid = self._row.get_value("TID", 0)
        self._infoTID = self._row.get_value("InfoTID", 0)

    def set_row(self, row: CSVRow):
        self._row = row

    def get_global_id(self) -> int:
        return self._globalId

    def get_instance_id(self) -> int:
        return GlobalID.get_instance_ID(self._globalId)

    def get_name(self) -> str:
        return self._row.get_name()

    def get_data_type(self) -> LogicDataType:
        return self._table.get_table_index()
