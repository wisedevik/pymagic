from enum import Enum
import socket
import asyncio
from typing import Optional

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
        self._client_socket.setblocking(False)
        self._receive_encrypter = RC4Encrypter(ENCRYPTION_KEY, "nonce")
        self._send_encrypter = RC4Encrypter(ENCRYPTION_KEY, "nonce")
        self._factory = LogicMagicMessageFactory()
        self._messageManager = messageManager
        self._send_lock = asyncio.Lock()
        self._outgoing_queue = asyncio.Queue()
        self._sending_task = None
        self._is_active = True
        asyncio.create_task(self._sending_loop())

    async def close(self):
        self._is_active = False
        if self._sending_task:
            self._sending_task.cancel()
            try:
                await self._sending_task
            except asyncio.CancelledError:
                pass

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

    async def send(self, message: PiranhaMessage):
        if not self._is_active:
            Debugger.warning("Messaging not active, message discarded")
            return
            
        await self._outgoing_queue.put(message)

    async def _send_message(self, message: PiranhaMessage):
        async with self._send_lock:
            if not self._is_active or self._client_socket.fileno() == -1:
                Debugger.warning("Socket closed, message discarded")
                return

            if message.get_encoding_length() == 0:
                message.encode()
            
            encoding_length = message.get_encoding_length()
            encoding_bytes = message.get_message_bytes()
            encrypted_bytes = self._send_encrypter.encrypt(encoding_bytes)
            encrypted_length = len(encrypted_bytes)

            stream = bytearray(HEADER_SIZE + encrypted_length)
            Messaging.write_header(message, stream, encrypted_length)
            stream[HEADER_SIZE:] = encrypted_bytes

            try:
                await self._send_all(stream)
                Debugger.warning(
                    f"Sent message {message.get_message_type()}"
                )
            except Exception as e:
                Debugger.error(f"Send failed: {str(e)}")
                self._is_active = False

    async def _send_all(self, data: bytearray):
        total_sent = 0
        while total_sent < len(data):
            try:
                sent = self._client_socket.send(data[total_sent:])
                if sent == 0:
                    raise ConnectionError("Socket connection broken")
                total_sent += sent
            except BlockingIOError:
                await asyncio.sleep(0.001)
            except OSError as e:
                Debugger.error(f"Connection error: {e}")
                raise

    async def on_receive(self, buffer: bytearray, length: int) -> int:
        if length < HEADER_SIZE:
            return 0

        message_type, encrypted_length, message_version = Messaging.read_header(buffer)
        required_length = HEADER_SIZE + encrypted_length

        if length < required_length:
            return 0

        encrypted_bytes = buffer[HEADER_SIZE:required_length]
        encoding_bytes = self._receive_encrypter.decrypt(encrypted_bytes)

        message = self._factory.create_message_by_type(message_type)
        if not message:
            Debugger.warning(f"Unhandled message type: {message_type}")
            return required_length

        try:
            message.get_byte_stream().set_byte_array(encoding_bytes, encrypted_length)
            message.set_message_version(message_version)
            message.decode()
            await self._messageManager.receive_message(message)
        except Exception as e:
            Debugger.error(f"Error processing message {message_type}: {str(e)}")

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