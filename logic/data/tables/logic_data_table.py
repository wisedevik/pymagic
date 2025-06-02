from logic.data.core.global_id import GlobalID
from logic.data.core.logic_data import LogicData
from logic.data.core.logic_data_type import LogicDataType
from titan.csv.csv_table import CSVTable
from titan.debug.debugger import Debugger
from titan.util.logic_array_list import LogicArrayList


class LogicDataTable:
    def __init__(self, table: CSVTable, index: LogicDataType) -> None:
        self._table = table
        self._table_idx = index
        self._items = LogicArrayList[LogicData | None]()
        self._is_loaded = False
        self._table_name = ""

        self.load_tables()

    def load_tables(self) -> None:
        for i in range(self._table.get_row_count()):
            self._items.add(self.create_item(self._table.get_row_at(i)))

    def create_references(self) -> None:
        if not self._is_loaded:
            for item in self._items:
                assert item is not None
                item.create_references()
            self._is_loaded = True

    def get_item_at(self, index: int) -> LogicData | None:
        return self._items[index]

    def set_table(self, table: CSVTable) -> None:
        self._table = table
        for i, item in enumerate(self._items):
            assert item is not None
            item.set_row(table.get_row_at(i))

    def set_name(self, name: str) -> None:
        self._table_name = name

    def get_item_count(self) -> int:
        return self._items.count

    def get_item_by_id(self, global_id: int) -> LogicData | None:
        instance_id = GlobalID.get_instance_id(global_id)
        if 0 <= instance_id < self._items.count:
            return self._items[instance_id]
        Debugger.warning("LogicDataTable.get_item_by_id() - Instance id out of bounds!")
        return None

    def get_data_by_name(self, name: str, caller: LogicData | None) -> LogicData | None:
        if name:
            for data in self._items:
                assert data is not None
                if data.get_name() == name:
                    return data

            if caller:
                Debugger.warning(
                    f"CSV row ({caller.get_name()}) has an invalid reference ({name})"
                )

        return None

    def get_table_name(self) -> str:
        return self._table_name

    def create_item(self, row) -> LogicData | None:
        item = None

        match self._table_idx:
            case LogicDataType.BUILDING:
                from logic.data.data_objects.logic_building_data import (
                    LogicBuildingData,
                )

                item = LogicBuildingData(row, self)
            case LogicDataType.BUILDING_CLASS:
                from logic.data.data_objects.logic_building_class_data import (
                    LogicBuildingClassData,
                )

                item = LogicBuildingClassData(row, self)
            case LogicDataType.RESOURCE:
                from logic.data.data_objects.logic_resource_data import (
                    LogicResourceData,
                )

                item = LogicResourceData(row, self)
            case LogicDataType.MISSION:
                from logic.data.data_objects.logic_mission_data import LogicMissionData

                item = LogicMissionData(row, self)
            case LogicDataType.GLOBAL:
                from logic.data.data_objects.logic_global_data import LogicGlobalData

                item = LogicGlobalData(row, self)
            case _:
                Debugger.error(f"Invalid data table id: {self._table_idx}")

        return item

    def get_table_index(self) -> LogicDataType:
        return self._table_idx
