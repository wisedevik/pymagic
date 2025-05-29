from titan.message.logic_message_factory import LogicMessageFactory
from titan.message.piranha_message import message_registry
from typing import Dict, Type, Optional

ENCRYPTION_KEY = "fhsd6f86f67rt8fw78fw789we78r9789wer6re"


class LogicMagicMessageFactory(LogicMessageFactory):
    def __init__(self) -> None:
        super().__init__()
        self._messages = message_registry

    def create_message_by_type(self, type: int):
        cls = self._messages.get(type)
        if cls:
            return cls()
