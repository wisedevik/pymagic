from logic.data.core.logic_data import LogicData
from titan.csv.csv_row import CSVRow


class LogicMissionData(LogicData):
    def __init__(self, row: CSVRow, table):
        super().__init__(row, table)
