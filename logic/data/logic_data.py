from logic.data.core.global_id import GlobalID
from logic.data.core.logic_data_type import LogicDataType
from titan.csv.csv_row import CSVRow


class LogicData:
    def __init__(self, row: CSVRow, table):
        self._row = row
        self._table = table
        self._icon_swf = ""
        self._icon_export_name = ""
        self._tid = ""
        self._info_tid = ""
        self._global_id = GlobalID.create_global_id(
            int(table.get_table_index()) + 1, table.get_item_count()
        )

    def create_references(self):
        self._icon_swf = self._row.get_value("IconSWF", 0)
        self._icon_export_name = self._row.get_value("IconExportName", 0)
        self._tid = self._row.get_value("TID", 0)
        self._info_tid = self._row.get_value("InfoTID", 0)

    def set_row(self, row: CSVRow):
        self._row = row

    def get_global_id(self) -> int:
        return self._global_id

    def get_instance_id(self) -> int:
        return GlobalID.get_instance_id(self._global_id)

    def get_name(self) -> str:
        return self._row.get_name()

    def get_data_type(self) -> LogicDataType:
        return self._table.get_table_index()
