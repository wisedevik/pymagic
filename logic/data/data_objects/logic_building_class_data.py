from logic.data.core.logic_data import LogicData
from titan.csv.csv_row import CSVRow


class LogicBuildingClassData(LogicData):
    def __init__(self, row: CSVRow, table):
        super().__init__(row, table)
        self.can_buy = False
        self.worker = False
        self.town_hall = False
        self.wall = False
        self.shop_category_resource = False
        self.shop_category_army = False
        self.shop_category_defense = False

    def create_references(self) -> None:
        super().create_references()

        self.can_buy = self.row.get_boolean_value("CanBuy", 0)

        self.worker = "Worker" == self.get_name()
        self.town_hall = "Town Hall" == self.get_name()
        self.wall = "Wall" == self.get_name()
        self.shop_category_resource = self.row.get_boolean_value(
            "ShopCategoryResource", 0
        )
        self.shop_category_army = self.row.get_boolean_value("ShopCategoryArmy", 0)
        self.shop_category_defense = self.row.get_boolean_value(
            "ShopCategoryDefense", 0
        )

    def can_buy(self) -> bool:
        return self.can_buy

    def is_worker(self) -> bool:
        return self.worker

    def is_town_hall(self) -> bool:
        return self.town_hall

    def is_wall(self) -> bool:
        return self.wall

    def is_shop_category_resource(self) -> bool:
        return self.shop_category_resource

    def is_shop_category_army(self) -> bool:
        return self.shop_category_army

    def is_shop_category_defense(self) -> bool:
        return self.shop_category_defense
