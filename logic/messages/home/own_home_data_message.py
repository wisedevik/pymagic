from titan.message.piranha_message import PiranhaMessage


class OwnHomeDataMessage(PiranhaMessage):
    def __init__(self) -> None:
        super().__init__()

    def encode(self): ...

    def get_message_type(self) -> int:
        return 24101

    def get_service_node_type(self) -> int:
        return 10
