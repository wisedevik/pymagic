from logic.home.listener.logic_home_change_listener import LogicHomeChangeListener
from logic.home.logic_base import LogicBase
from titan.datastream.checksum_encoder import ChecksumEncoder
from titan.math.logic_long import LogicLong


class LogicClientHome(LogicBase):
    def __init__(self) -> None:
        super().__init__()
        self.listener = LogicHomeChangeListener()
        self.id = LogicLong()
        self.home_json = ""
        self.shield_duration_seconds = 0
        self.defense_rating = 0
        self.defense_kfactor = 0

    def encode(self, encoder: ChecksumEncoder):
        super().encode(encoder)
