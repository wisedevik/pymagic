from titan.message.logic_message_factory import LogicMessageFactory
from titan.message.piranha_message import message_registry

ENCRYPTION_KEY = "fhsd6f86f67rt8fw78fw789we78r9789wer6re"


class LogicMagicMessageFactory(LogicMessageFactory):
    def __init__(self) -> None:
        super().__init__()
        self._messages = message_registry

    def create_message_by_type(self, message_type: int):
        cls = self._messages.get(message_type)
        if cls:
            return cls()
