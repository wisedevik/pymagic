from logic.data.core.logic_data import LogicData
from titan.csv.csv_row import CSVRow


class LogicBuildingData(LogicData):
    def __init__(self, row: CSVRow, table):
        super().__init__(row, table)
        self._width = 0
        self._height = 0

    def create_references(self):
        super().create_references()

        self._width = self._row.get_integer_value("Width", 0)
        self._height = self._row.get_integer_value("Height", 0)

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height
