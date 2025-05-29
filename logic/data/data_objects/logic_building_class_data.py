from logic.data.core.logic_data import LogicData
from titan.csv.csv_row import CSVRow


class LogicBuildingClassData(LogicData):
    def __init__(self, row: CSVRow, table):
        super().__init__(row, table)
        self._can_buy = False
        self._worker = False
        self._town_hall = False
        self._wall = False
        self._shop_category_resource = False
        self._shop_category_army = False
        self._shop_category_defense = False

    def create_references(self) -> None:
        super().create_references()

        self._can_buy = self._row.get_boolean_value("CanBuy", 0)

        self._worker = "Worker" == self.get_name()
        self._town_hall = "Town Hall" == self.get_name()
        self._wall = "Wall" == self.get_name()
        self._shop_category_resource = self._row.get_boolean_value(
            "ShopCategoryResource", 0
        )
        self._shop_category_army = self._row.get_boolean_value("ShopCategoryArmy", 0)
        self._shop_category_defense = self._row.get_boolean_value(
            "ShopCategoryDefense", 0
        )

    def can_buy(self) -> bool:
        return self._can_buy

    def is_worker(self) -> bool:
        return self._worker

    def is_town_hall(self) -> bool:
        return self._town_hall

    def is_wall(self) -> bool:
        return self._wall

    def is_shop_category_resource(self) -> bool:
        return self._shop_category_resource

    def is_shop_category_army(self) -> bool:
        return self._shop_category_army

    def is_shop_category_defense(self) -> bool:
        return self._shop_category_defense
