from titan.debug.debugger import Debugger
from titan.message.piranha_message import PiranhaMessage


class MessageManager:
    def __init__(self, connection):
        self._connection = connection

    def receive_message(self, message: PiranhaMessage):
        Debugger.print(f"[MessageManager.receive_message] message_type={message.get_message_type()}")
