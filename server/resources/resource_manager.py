from logic.data.tables.logic_data_tables import LogicDataTables
from logic.data.resources.logic_resources import LogicResources
from titan.csv.csv_node import CSVNode


class ResourceManager:
    @staticmethod
    def load_game_resources():
        LogicDataTables.init()

        resources = LogicResources.create_data_table_resources_array()
        for i in range(resources.count):
            file_name = resources[i].get_file_name()

            with open(file_name, "r", encoding="utf-8") as f:
                lines = f.readlines()

            LogicResources.load(resources, i, CSVNode(lines, file_name))
