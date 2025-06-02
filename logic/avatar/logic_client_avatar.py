from typing import cast
from logic.avatar.logic_avatar import LogicAvatar
from logic.data.data_objects.logic_mission_data import LogicMissionData
from logic.data.tables.logic_data_tables import LogicDataTables
from logic.helper.byte_stream_helper import ByteStreamHelper
from titan.datastream.checksum_encoder import ChecksumEncoder
from titan.math.logic_long import LogicLong
from logic.data.core.logic_data_type import LogicDataType


class LogicClientAvatar(LogicAvatar):
    def __init__(self) -> None:
        super().__init__()
        super().init_base()
        self.diamonds = 0
        self.free_diamonds = 0

    @staticmethod
    def get_default_avatar():
        avatar = LogicClientAvatar()

        # TODO: Replace hardcode to LogicGlobals data
        avatar.diamonds = 5000
        avatar.free_diamonds = 5000

        avatar.set_resource_count(LogicDataTables.get_gold_data(), 1000)
        avatar.set_resource_count(LogicDataTables.get_elixir_data(), 1000)

        table = LogicDataTables.get_table(LogicDataType.MISSION)

        for i in range(table.get_item_count()):
            missionData: LogicMissionData = cast(
                LogicMissionData, LogicDataTables.get_data_by_id(21000000 + i)
            )
            if missionData:
                avatar.set_mission_completed(missionData, True)

        return avatar

    def encode(self, encoder: ChecksumEncoder):
        super().encode(encoder)

        encoder.write_long(LogicLong(0, 32))
        encoder.write_long(LogicLong(0, 32))
        encoder.write_boolean(False)
        encoder.write_boolean(False)
        encoder.write_boolean(False)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_string("MagicPy")  # Name
        encoder.write_string("")
        encoder.write_int(1)
        encoder.write_int(0)
        encoder.write_int(self.diamonds)  # Diamonds
        encoder.write_int(self.free_diamonds)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_boolean(False)
        encoder.write_int(0)

        encoder.write_int(0)
        encoder.write_int(self.resource_count.count)
        for item in self.resource_count:
            item.encode(encoder)

        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)

        encoder.write_int(self.mission_completed.count)  # skip tutorial
        for item in self.mission_completed:
            ByteStreamHelper.write_data_reference(encoder, item)

        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
