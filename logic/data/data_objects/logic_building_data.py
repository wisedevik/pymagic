from logic.data.data_objects.logic_building_class_data import LogicBuildingClassData
from logic.data.core.logic_data import LogicData
from titan.csv.csv_row import CSVRow
from titan.debug.debugger import Debugger


class LogicBuildingData(LogicData):
    def __init__(self, row: CSVRow, table):
        super().__init__(row, table)
        self._building_class = None
        self._upgrade_level_count = 0
        self._width = 0
        self._height = 0
        self._produces_units_of_type = 0
        self._damage = []
        self._housingSpace = []

    def create_references(self):
        super().create_references()
        from logic.data.tables.logic_data_tables import LogicDataTables

        self._building_class = LogicDataTables.get_building_class_by_name(
            self._row.get_value("BuildingClass", 0), self
        )
        if self._building_class is None:
            Debugger.error(f"Building class is not defined for {self._row.get_name()}")

        self._width = self._row.get_integer_value("Width", 0)
        self._height = self._row.get_integer_value("Height", 0)
        self._produces_units_of_type = self._row.get_integer_value(
            "ProducesUnitsOfType", 0
        )

        upgLvlCnt = self._upgrade_level_count = self._row.get_longest_array_size()
        self._damage = [0] * upgLvlCnt
        self._housingSpace = [0] * upgLvlCnt

        for i in range(upgLvlCnt):
            self._damage[i] = self._row.get_clamped_integer_value("Damage", i)
            self._housingSpace[i] = self._row.get_clamped_integer_value(
                "HousingSpace", i
            )

    def get_building_class(self) -> LogicBuildingClassData:
        assert self._building_class is not None
        return self._building_class

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_upgrade_level_count(self):
        return self._upgrade_level_count

    def get_unit_storage_capacity(self, level: int):
        return self._housingSpace[level]
