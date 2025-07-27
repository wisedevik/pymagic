from titan.message.piranha_message import PiranhaMessage
from titan.math.logic_long import LogicLong


class LoginMessage(PiranhaMessage):
    MESSAGE_TYPE = 10101
    def __init__(self) -> None:
        super().__init__()
        self.account_id = LogicLong()
        self.pass_token = ""
        self.major_version = 0
        self.minor_version = 0
        self.build = 0

    def decode(self):
        super().decode()
        self.account_id = self.stream.read_long()
        self.pass_token = self.stream.read_string()
        self.major_version = self.stream.read_int()
        self.minor_version = self.stream.read_int()
        self.build = self.stream.read_int()

    def get_message_type(self) -> int:
        return self.MESSAGE_TYPE

    def get_service_node_type(self) -> int:
        return 1

    def get_version(self) -> str:
        return f"{self.major_version}.{self.build}.{self.minor_version}"
