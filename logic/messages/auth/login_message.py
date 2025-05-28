from logic.messages.message_registry import piranha_message
from titan.debug.debugger import Debugger
from titan.message.piranha_message import PiranhaMessage
from titan.math.logic_long import LogicLong

MESSAGE_TYPE = 10101


@piranha_message(MESSAGE_TYPE)
class LoginMessage(PiranhaMessage):
    def __init__(self) -> None:
        super().__init__()
        self._account_id = LogicLong()
        self.pass_token = ""
        self._majorVersion = 0
        self._minorVersion = 0
        self._build = 0

    def decode(self):
        super().decode()
        self._account_id = self.stream.read_long()
        self.pass_token = self.stream.read_string()
        self._majorVersion = self.stream.read_int()
        self._minorVersion = self.stream.read_int()
        self._build = self.stream.read_int()

    def get_message_type(self) -> int:
        return MESSAGE_TYPE

    def get_service_node_type(self) -> int:
        return 1

    def get_version(self) -> str:
        return f"{self._majorVersion}.{self._build}.{self._minorVersion}"
