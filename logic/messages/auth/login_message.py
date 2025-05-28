from logic.messages.message_registry import piranha_message
from titan.debug.debugger import Debugger
from titan.message.piranha_message import PiranhaMessage

MESSAGE_TYPE = 10101

@piranha_message(MESSAGE_TYPE)
class LoginMessage(PiranhaMessage):
    def __init__(self) -> None:
        super().__init__()

    def get_message_type(self) -> int:
        return MESSAGE_TYPE

    def get_service_node_type(self) -> int:
        return 1
