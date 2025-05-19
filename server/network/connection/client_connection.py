import socket
import asyncio

from server.network.protocol.messaging import Messaging
from titan.debug.debugger import Debugger

class ClientConnection:
    def __init__(self, socket: socket.socket) -> None:
        self._client_socket = socket
        self._messaging = Messaging(self._client_socket)

        self._receive_buffer = bytearray(8192)

    async def receive(self):
        loop = asyncio.get_running_loop()

        recv_idx = 0
        while True:
            data = await loop.sock_recv(self._client_socket, 4096)
            if not data:
                break

            self._receive_buffer[recv_idx:recv_idx+len(data)] = data
            recv_idx += len(data)

            self._messaging.on_receive(self._receive_buffer, recv_idx)
