from logic.data.data_objects.logic_building_class_data import LogicBuildingClassData
from logic.data.core.logic_data import LogicData
from titan.csv.csv_row import CSVRow
from titan.debug.debugger import Debugger


class LogicBuildingData(LogicData):
    def __init__(self, row: CSVRow, table):
        super().__init__(row, table)
        self.building_class = None
        self.upgrade_level_count = 0
        self.width = 0
        self.height = 0
        self.produces_units_of_type = 0
        self.damage = []
        self.housing_space = []

    def create_references(self):
        super().create_references()
        from logic.data.tables.logic_data_tables import LogicDataTables

        self.building_class = LogicDataTables.get_building_class_by_name(
            self.row.get_value("BuildingClass", 0), self
        )
        if self.building_class is None:
            Debugger.error(f"Building class is not defined for {self.row.get_name()}")

        self.width = self.row.get_integer_value("Width", 0)
        self.height = self.row.get_integer_value("Height", 0)
        self.produces_units_of_type = self.row.get_integer_value(
            "ProducesUnitsOfType", 0
        )

        upg_lvl_cnt = self.upgrade_level_count = self.row.get_longest_array_size()
        self.damage = [0] * upg_lvl_cnt
        self.housing_space = [0] * upg_lvl_cnt

        for i in range(upg_lvl_cnt):
            self.damage[i] = self.row.get_clamped_integer_value("Damage", i)
            self.housing_space[i] = self.row.get_clamped_integer_value(
                "HousingSpace", i
            )

    def get_building_class(self) -> LogicBuildingClassData:
        assert self.building_class is not None
        return self.building_class

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_upgrade_level_count(self):
        return self.upgrade_level_count

    def get_unit_storage_capacity(self, level: int):
        return self.housing_space[level]
