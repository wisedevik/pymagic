from logic.data.tables.logic_data_table_resource import LogicDataTableResource
from logic.data.tables.logic_data_tables import TABLE_COUNT, LogicDataTables
from logic.data.core.logic_data_type import LogicDataType
from titan.csv.csv_node import CSVNode
from titan.debug.debugger import Debugger
from titan.util.logic_array_list import LogicArrayList


class LogicResources:
    @staticmethod
    def create_data_table_resources_array() -> LogicArrayList[LogicDataTableResource]:
        arrayList = LogicArrayList[LogicDataTableResource](TABLE_COUNT)
        arrayList.add(LogicDataTableResource("server/assets/csv_logic/buildings.csv", LogicDataType.BUILDING, 0))
        arrayList.add(LogicDataTableResource("server/assets/csv_logic/resources.csv", LogicDataType.RESOURCE, 0))
        return arrayList

    @staticmethod
    def load(resources: LogicArrayList[LogicDataTableResource], idx: int, node: CSVNode):
        resource = resources[idx]

        match resource.get_type():
            case 0:
                LogicDataTables.init_data_table(node, resource.get_table_index())
            case _:
                Debugger.error("LogicResources.Invalid resource type");

        if (resources.count - 1 == idx):
            LogicDataTables.create_references()
