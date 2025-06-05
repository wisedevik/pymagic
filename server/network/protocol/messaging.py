import asyncio
from logic.messages.logic_magic_message_factory import (
    LogicMagicMessageFactory,
)
from titan.crypto.rc4_encrypter import RC4Encrypter
from titan.debug.debugger import Debugger
from titan.message.piranha_message import PiranhaMessage
from server.config import Configuration


class Messaging:
    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        message_manager,
    ) -> None:
        self.reader = reader
        self.writer = writer
        self.receive_encrypter = RC4Encrypter(
            Configuration.crypto.encryption_key, Configuration.crypto.nonce
        )
        self.send_encrypter = RC4Encrypter(
            Configuration.crypto.encryption_key, Configuration.crypto.nonce
        )
        self.factory = LogicMagicMessageFactory()
        self.message_manager = message_manager

    async def send(self, message: PiranhaMessage):
        if message.get_encoding_length() == 0:
            message.encode()

        encoding_bytes = message.get_message_bytes()
        encrypted_bytes = self.send_encrypter.encrypt(encoding_bytes)
        encrypted_length = len(encrypted_bytes)

        stream = bytearray(7 + encrypted_length)
        self.write_header(message, stream, encrypted_length)
        stream[7:] = encrypted_bytes

        self.writer.write(stream)
        await self.writer.drain()
        Debugger.warning(f"Sent message {message.get_message_type()}")

    async def on_receive(self, buffer: bytearray, length: int) -> int:
        if length < 7:
            return 0

        message_type, encrypted_length, message_version = self.read_header(buffer)
        required_length = 7 + encrypted_length

        if length < required_length:
            return 0

        encrypted_bytes = buffer[7:required_length]
        encoding_bytes = self.receive_encrypter.decrypt(encrypted_bytes)

        message = self.factory.create_message_by_type(message_type)
        if not message:
            Debugger.warning(f"Unhandled message type: {message_type}")
            return required_length

        message.get_byte_stream().set_byte_array(encoding_bytes, encrypted_length)
        message.set_message_version(message_version)
        message.decode()
        await self.message_manager.receive_message(message)

        return required_length

    @staticmethod
    def read_header(stream: bytearray) -> tuple[int, int, int]:
        message_type = (stream[0] << 8) | stream[1]
        length = (stream[2] << 16) | (stream[3] << 8) | stream[4]
        message_version = (stream[5] << 8) | stream[6]
        return message_type, length, message_version

    @staticmethod
    def write_header(message: PiranhaMessage, stream: bytearray, encrypted_length: int):
        message_type = message.get_message_type()
        message_version = message.get_message_version()

        stream[0] = (message_type >> 8) & 0xFF
        stream[1] = message_type & 0xFF
        stream[2] = (encrypted_length >> 16) & 0xFF
        stream[3] = (encrypted_length >> 8) & 0xFF
        stream[4] = encrypted_length & 0xFF
        stream[5] = (message_version >> 8) & 0xFF
        stream[6] = message_version & 0xFF
