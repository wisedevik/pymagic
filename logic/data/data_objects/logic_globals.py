from logic.data.tables import LogicDataTable
from logic.data.data_objects.logic_global_data import LogicGlobalData


class LogicGlobals(LogicDataTable):
    def __init__(self, table, index):
        super().__init__(table, index)

        self.starting_diamonds = 0
        self.starting_elixir = 0
        self.starting_gold = 0

    def create_references(self):
        super().create_references()
        self.starting_diamonds = self.get_int_value("STARTING_DIAMONDS")
        self.starting_elixir = self.get_int_value("STARTING_ELIXIR")
        self.starting_gold = self.get_int_value("STARTING_GOLD")

    def get_global_data(self, name) -> LogicGlobalData:
        from logic.data.tables import LogicDataTables

        return LogicDataTables.get_global_by_name(name)

    def get_bool_value(self, name):
        self.get_global_data(name).get_boolean_value()

    def get_int_value(self, name):
        self.get_global_data(name).get_number_value()

    def get_value(self, name):
        self.get_global_data(name).get_text_value()
