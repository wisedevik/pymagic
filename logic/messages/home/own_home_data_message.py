from titan.message.piranha_message import PiranhaMessage

MESSAGE_TYPE = 24101


class OwnHomeDataMessage(PiranhaMessage):
    def __init__(self) -> None:
        super().__init__()

    def encode(self): ...

    def get_message_type(self) -> int:
        return MESSAGE_TYPE

    def get_service_node_type(self) -> int:
        return 10
