from titan.message.logic_message_factory import LogicMessageFactory
from logic.messages.message_registry import message_registry

ENCRYPTION_KEY = "fhsd6f86f67rt8fw78fw789we78r9789wer6re"


class LogicMagicMessageFactory(LogicMessageFactory):
    def __init__(self) -> None:
        super().__init__()
        self._messages = message_registry

    def create_message_by_type(self, type: int):
        cls = self._messages.get(type)
        return cls() if cls else None
