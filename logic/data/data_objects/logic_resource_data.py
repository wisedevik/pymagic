from logic.data.core.logic_data import LogicData
from titan.csv.csv_row import CSVRow


class LogicResourceData(LogicData):
    def __init__(self, row: CSVRow, table):
        super().__init__(row, table)
        self._premium_currency = False

    def create_references(self) -> None:
        self._premium_currency = self._row.get_boolean_value("PremiumCurrency", 0)
        super().create_references()

    def is_premium_currency(self) -> bool:
        return self._premium_currency
