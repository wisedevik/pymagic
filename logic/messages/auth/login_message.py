from titan.message.piranha_message import PiranhaMessage
from titan.math.logic_long import LogicLong


class LoginMessage(PiranhaMessage):
    def __init__(self) -> None:
        super().__init__()
        self._account_id = LogicLong()
        self.pass_token = ""
        self._major_version = 0
        self._minor_version = 0
        self._build = 0

    def decode(self):
        super().decode()
        self._account_id = self.stream.read_long()
        self.pass_token = self.stream.read_string()
        self._major_version = self.stream.read_int()
        self._minor_version = self.stream.read_int()
        self._build = self.stream.read_int()

    def get_message_type(self) -> int:
        return 10101

    def get_service_node_type(self) -> int:
        return 1

    def get_version(self) -> str:
        return f"{self._major_version}.{self._build}.{self._minor_version}"
