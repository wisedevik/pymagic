from typing import cast
from logic.avatar.logic_avatar import LogicAvatar
from logic.data.data_objects.logic_mission_data import LogicMissionData
from logic.data.tables.logic_data_table import LogicDataTable
from logic.data.tables.logic_data_tables import LogicDataTables
from titan.datastream.checksum_encoder import ChecksumEncoder
from titan.math.logic_long import LogicLong


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
        avatar.diamonds = 500
        avatar.free_diamonds = 500

        avatar.set_resource_count(LogicDataTables.get_gold_data(), 1000)
        avatar.set_resource_count(LogicDataTables.get_elixir_data(), 900)

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
        encoder.write_string("Name") # Name
        encoder.write_string("")
        encoder.write_int(1)
        encoder.write_int(0)
        encoder.write_int(1) # Diamonds
        encoder.write_int(0)
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
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)

        listik = list(range(21000000, 21000013))
        encoder.write_int(len(listik)) # skip tutorial
        for item in listik:
            encoder.write_int(item)

        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
        encoder.write_int(0)
