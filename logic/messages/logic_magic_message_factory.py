from titan.message.logic_message_factory import LogicMessageFactory
from titan.message.piranha_message import message_registry


class LogicMagicMessageFactory(LogicMessageFactory):
    def __init__(self) -> None:
        super().__init__()
        self.messages = message_registry

    def create_message_by_type(self, message_type: int):
        cls = self.messages.get(message_type)
        if cls:
            return cls()
