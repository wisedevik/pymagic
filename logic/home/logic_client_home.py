from logic.home.listener.logic_home_change_listener import LogicHomeChangeListener
from logic.home.logic_base import LogicBase
from titan.datastream.checksum_encoder import ChecksumEncoder
from titan.math.logic_long import LogicLong


class LogicClientHome(LogicBase):
    def __init__(self) -> None:
        super().__init__()
        self.listener = LogicHomeChangeListener()
        self.id = LogicLong(0, 1)
        self.home_json = """"""
        self.shield_duration_seconds = 0
        self.defense_rating = 0
        self.defense_kfactor = 0

    def set_home_json(self, json):
        self.home_json = json

    def encode(self, encoder: ChecksumEncoder):
        super().encode(encoder)
        encoder.write_long(self.id)
        encoder.write_string(self.home_json)
        encoder.write_int(self.shield_duration_seconds)
        encoder.write_int(self.defense_rating)
        encoder.write_int(self.defense_kfactor)
