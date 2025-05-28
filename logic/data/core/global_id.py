class GlobalID:
    @staticmethod
    def create_global_ID(type_id: int, instance_id: int) -> int:
        return (type_id << 16) | instance_id

    @staticmethod
    def get_instance_ID(global_id: int) -> int:
        return global_id & 0xFFFF

    @staticmethod
    def get_class_id(global_id: int) -> int:
        return (global_id >> 24) & 0xFF
