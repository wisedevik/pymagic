from logic.avatar.logic_client_avatar import LogicClientAvatar
from titan.message.piranha_message import PiranhaMessage
from logic.home import LogicClientHome


class OwnHomeDataMessage(PiranhaMessage):
    MESSAGE_TYPE = 24101

    def __init__(self) -> None:
        super().__init__()
        self.seconds_since_last_save: int = 0
        self.home: LogicClientHome | None = None
        self.avatar: LogicClientAvatar | None = None

    def set_seconds_since_last_save(self, s: int):
        self.seconds_since_last_save = s

    def set_home(self, home: LogicClientHome):
        self.home = home

    def set_avatar(self, avatar: LogicClientAvatar):
        self.avatar = avatar

    def encode(self):
        super().encode()
        self.stream.write_int(self.seconds_since_last_save)
        self.home.encode(self.stream)
        self.avatar.encode(self.stream)

    def get_message_type(self) -> int:
        return self.MESSAGE_TYPE

    def get_service_node_type(self) -> int:
        return 10
