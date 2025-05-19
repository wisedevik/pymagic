import socket

from titan.debug.debugger import Debugger

HEADER_SIZE = 7

class Messaging:
    def __init__(self, client_socket: socket.socket) -> None:
        self._client_socket = client_socket

    def on_receive(self, buffer: bytearray, length: int):
        if (length >= HEADER_SIZE):
            (message_type, encrypted_length, message_version) = Messaging.read_header(buffer)

            Debugger.print(f"[Messaging.on_receive] New message with type={message_type}, length={encrypted_length}, message_version={message_version}")


    @staticmethod
    def read_header(stream) -> tuple[int, int, int]:
        message_type = (stream[0] << 8) | stream[1]
        length = (stream[2] << 16) | (stream[3] << 8) | stream[4]
        message_version = (stream[5] << 8) | stream[6]
        return message_type, length, message_version
