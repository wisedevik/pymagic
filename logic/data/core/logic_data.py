from logic.data.core.global_id import GlobalID
from logic.data.core.logic_data_type import LogicDataType
from titan.csv.csv_row import CSVRow


class LogicData:
    def __init__(self, row: CSVRow, table):
        self.row = row
        self.table = table
        self.icon_swf = ""
        self.icon_export_name = ""
        self.tid = ""
        self.info_tid = ""
        self.global_id = GlobalID.create_global_id(
            int(table.get_table_index()) + 1, table.get_item_count()
        )

    def create_references(self) -> None:
        self.icon_swf = self.row.get_value("IconSWF", 0)
        self.icon_export_name = self.row.get_value("IconExportName", 0)
        self.tid = self.row.get_value("TID", 0)
        self.info_tid = self.row.get_value("InfoTID", 0)

    def set_row(self, row: CSVRow):
        self.row = row

    def get_global_id(self) -> int:
        return self.global_id

    def get_instance_id(self) -> int:
        return GlobalID.get_instance_id(self.global_id)

    def get_name(self) -> str:
        return self.row.get_name()

    def get_data_type(self) -> LogicDataType:
        return self.table.get_table_index()
