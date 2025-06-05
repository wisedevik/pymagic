from logic.data.core.logic_data import LogicData
from titan.csv.csv_row import CSVRow


class LogicGlobalData(LogicData):
    def __init__(self, row: CSVRow, table):
        super().__init__(row, table)
        self.number_value = 0
        self.boolean_value = False
        self.text_value = ""
        self.number_array = []
        self.string_array = []

    def create_references(self):
        super().create_references()

        size = self.row.get_longest_array_size()
        self.number_array = [0] * size
        self.string_array = [""] * size

        self.number_value = self.row.get_integer_value("NumberValue", 0)
        self.boolean_value = self.row.get_boolean_value("BooleanValue", 0)
        self.text_value = self.row.get_value("TextValue", 0)

        for i in range(size):
            self.number_array[i] = self.row.get_integer_value("NumberArray", i)
            self.string_array[i] = self.row.get_value("StringArray", i)

    def get_number_value(self):
        return self.number_value

    def get_boolean_value(self):
        return self.boolean_value

    def get_text_value(self):
        return self.text_value

    def get_number_array_value(self, index):
        return self.number_array[index]

    def get_text_array_value(self, index):
        return self.string_array[index]
