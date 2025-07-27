class GlobalID:
    @staticmethod
    def create_global_id(type_id: int, instance_id: int) -> int:
        return 1000000 * type_id + instance_id

    @staticmethod
    def get_instance_id(global_id: int) -> int:
        return global_id % 1000000

    @staticmethod
    def get_class_id(global_id: int) -> int:
        return global_id // 1000000
