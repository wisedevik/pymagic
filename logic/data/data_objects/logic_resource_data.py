from logic.data.core.logic_data import LogicData
from titan.csv.csv_row import CSVRow


class LogicResourceData(LogicData):
    def __init__(self, row: CSVRow, table):
        super().__init__(row, table)
        self.premium_currency = False

    def create_references(self) -> None:
        self.premium_currency = self.row.get_boolean_value("PremiumCurrency", 0)
        super().create_references()

    def is_premium_currency(self) -> bool:
        return self.premium_currency
