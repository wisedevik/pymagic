from logic.avatar.logic_client_avatar import LogicClientAvatar
from titan.message.piranha_message import PiranhaMessage
from logic.home import LogicClientHome


class OwnHomeDataMessage(PiranhaMessage):
    def __init__(self) -> None:
        super().__init__()

    def encode(self):
        super().encode()
        self.stream.write_int(0)
        LogicClientHome().encode(self.stream)
        LogicClientAvatar().encode(self.stream)

    def get_message_type(self) -> int:
        return 24101

    def get_service_node_type(self) -> int:
        return 10
