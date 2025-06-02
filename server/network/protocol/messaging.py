from enum import member
from re import L
import socket
import asyncio

from logic.messages.logic_magic_message_factory import (
    ENCRYPTION_KEY,
    LogicMagicMessageFactory,
)
from titan.crypto.rc4_encrypter import RC4Encrypter
from titan.debug.debugger import Debugger
from titan.message.piranha_message import PiranhaMessage

HEADER_SIZE = 7


class Messaging:
    def __init__(self, client_socket: socket.socket, messageManager) -> None:
        self._client_socket = client_socket
        self._receive_encrypter = RC4Encrypter(ENCRYPTION_KEY, "nonce")
        self._send_encrypter = RC4Encrypter(ENCRYPTION_KEY, "nonce")
        self._factory = LogicMagicMessageFactory()
        self._messageManager = messageManager

        self._send_lock = asyncio.Lock()

    async def on_receive(self, buffer: bytearray, length: int):
        if length >= HEADER_SIZE:
            (message_type, encrypted_length, message_version) = Messaging.read_header(
                buffer
            )

<<<<<<< Updated upstream
            if length - HEADER_SIZE >= encrypted_length:
                encrypted_bytes = bytearray(encrypted_length)
                encoding_bytes = bytearray(encrypted_length)

                encrypted_bytes[:] = buffer[
                    HEADER_SIZE : HEADER_SIZE + encrypted_length
                ]

                encoding_bytes = self._receive_encrypter.decrypt(encrypted_bytes)

                message = self._factory.create_message_by_type(message_type)
                if message is not None:
                    message.get_byte_stream().set_byte_array(
                        encoding_bytes, encrypted_length
                    )
                    message.set_message_version(message_version)
                    message.decode()

                    await self._messageManager.receive_message(message)

                return encrypted_length + HEADER_SIZE

        return 0
=======
    async def _sending_loop(self):
        while self._is_active:
            try:
                message = await self._outgoing_queue.get()
                if not self._is_active:
                    break

                await self._send_message(message)
                self._outgoing_queue.task_done()

                await asyncio.sleep(0.001)

            except asyncio.CancelledError:
                break
            except Exception as e:
                Debugger.error(f"Sending loop error: {e}")
                await asyncio.sleep(0.1)
>>>>>>> Stashed changes

    async def send(self, message: PiranhaMessage):
        if not self._client_socket:
            Debugger.print("[Messaging] Socket not connected")
            return
<<<<<<< Updated upstream
=======

        await self._outgoing_queue.put(message)
>>>>>>> Stashed changes

        if message.get_encoding_length() == 0:
            message.encode()

<<<<<<< Updated upstream
        encoding_length = message.get_encoding_length()
        encoding_bytes = message.get_message_bytes()
=======
            if message.get_encoding_length() == 0:
                message.encode()

            encoding_length = message.get_encoding_length()
            encoding_bytes = message.get_message_bytes()
            encrypted_bytes = self._send_encrypter.encrypt(encoding_bytes)
            encrypted_length = len(encrypted_bytes)
>>>>>>> Stashed changes

        encrypted_bytes = self._send_encrypter.encrypt(encoding_bytes)

<<<<<<< Updated upstream
        stream = bytearray(encoding_length + HEADER_SIZE)
        Messaging.write_header(message, stream, encoding_length)
        stream[HEADER_SIZE:] = encrypted_bytes

        await self._send_all(stream)
        Debugger.warning(f"Sent message with type {message.get_message_type()} length={message.get_encoding_length()}")
=======
            try:
                await self._send_all(stream)
                Debugger.warning(f"Sent message with type {message.get_message_type()}")
            except Exception as e:
                Debugger.error(f"Send failed: {str(e)}")
                self._is_active = False
>>>>>>> Stashed changes

    async def _send_all(self, data: bytearray):
        total_sent = 0
        while total_sent < len(data):
            sent = self._client_socket.send(data[total_sent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            total_sent += sent

    @staticmethod
    def read_header(stream) -> tuple[int, int, int]:
        message_type = (stream[0] << 8) | stream[1]
        length = (stream[2] << 16) | (stream[3] << 8) | stream[4]
        message_version = (stream[5] << 8) | stream[6]
        return message_type, length, message_version

    @staticmethod
    def write_header(message: PiranhaMessage, stream: bytearray, length: int):
        message_type = message.get_message_type()
        message_version = message.get_message_version()
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
        stream[0] = (message_type >> 8) & 0xFF
        stream[1] = message_type & 0xFF
        stream[2] = (length >> 16) & 0xFF
        stream[3] = (length >> 8) & 0xFF
        stream[4] = length & 0xFF
        stream[5] = (message_version >> 8) & 0xFF
        stream[6] = message_version & 0xFF
