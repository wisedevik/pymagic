from titan.math.logic_long import LogicLong
from titan.message.piranha_message import PiranhaMessage


class LoginOkMessage(PiranhaMessage):
    def __init__(self) -> None:
        super().__init__()
        self.account_id = LogicLong()
        self.home_id = LogicLong()
        self.pass_token = ""
        self.major_version = 0
        self.build = 0
        self.minor_version = 0
        self.environment = ""

    def encode(self):
        super().encode()
        self.stream.write_long(self.account_id)
        self.stream.write_long(self.home_id)
        self.stream.write_string(self.pass_token)
        self.stream.write_string("")
        self.stream.write_string("")
        self.stream.write_int(self.major_version)
        self.stream.write_int(self.build)
        self.stream.write_int(self.minor_version)
        self.stream.write_string(self.environment)
        self.stream.write_int(0)
        self.stream.write_int(0)
        self.stream.write_int(0)
        self.stream.write_string("")
        self.stream.write_string("")
        self.stream.write_string("")
        self.stream.write_int(0)
        self.stream.write_string("")

    def get_message_type(self) -> int:
        return 20104
