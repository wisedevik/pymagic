import socket

from logic.messages.logic_magic_message_factory import ENCRYPTION_KEY, LogicMagicMessageFactory
from titan.crypto.rc4_encrypter import RC4Encrypter
from titan.debug.debugger import Debugger

HEADER_SIZE = 7

class Messaging:
    def __init__(self, client_socket: socket.socket, messageManager) -> None:
        self._client_socket = client_socket
        self._receive_encrypter = RC4Encrypter(ENCRYPTION_KEY, "nonce")
        self._send_encrypter = RC4Encrypter(ENCRYPTION_KEY, "nonce")
        self._factory = LogicMagicMessageFactory()
        self._messageManager = messageManager

    def on_receive(self, buffer: bytearray, length: int):
        if (length >= HEADER_SIZE):
            (message_type, encrypted_length, message_version) = Messaging.read_header(buffer)
            Debugger.print(f"[Messaging.on_receive] New message with type={message_type}, length={encrypted_length}, message_version={message_version}")

            if (length - HEADER_SIZE >= encrypted_length):
                encrypted_bytes = bytearray(encrypted_length)
                encoding_bytes = bytearray(encrypted_length)

                encrypted_bytes[:] = buffer[HEADER_SIZE:HEADER_SIZE + encrypted_length]

                encoding_bytes = self._receive_encrypter.decrypt(encrypted_bytes)

                message = self._factory.create_message_by_type(message_type)
                if message is not None:
                    message.get_byte_stream().set_byte_array(encoding_bytes, encrypted_length)
                    message.set_message_version(message_version)
                    message.decode()

                    self._messageManager.receive_message(message)

                return encrypted_length + HEADER_SIZE

        return 0


    @staticmethod
    def read_header(stream) -> tuple[int, int, int]:
        message_type = (stream[0] << 8) | stream[1]
        length = (stream[2] << 16) | (stream[3] << 8) | stream[4]
        message_version = (stream[5] << 8) | stream[6]
        return message_type, length, message_version
