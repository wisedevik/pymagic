from ast import Add
import socket
import asyncio

from server.network.connection.client_connection_manager import ClientConnectionManager
from titan.debug.debugger import Debugger

class TCPGateway:
    def __init__(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(("0.0.0.0", 9339))
        self._connection_manager = ClientConnectionManager()

        self._listen_task = None
        self._running = False

    async def start(self) -> None:
        self._socket.listen(100)
        self._socket.setblocking(False)

        Debugger.print(f"[TCPGateway.start] Server is listeting on {self._socket.getsockname()})")

        self._running = True
        self._listen_task = asyncio.create_task(self._handle_async())


    async def _handle_async(self):
        loop = asyncio.get_running_loop()
        while self._running:
            try:
                client_sock, addr = await loop.sock_accept(self._socket)
                self._connection_manager.on_connect(client_sock, addr)

            except asyncio.CancelledError:
                break
            except Exception as e:
                Debugger.error(f"Unexpected error: {e}")
