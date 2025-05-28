from ast import Add
import socket
import asyncio

from config import Config
from server.network.connection.client_connection_manager import ClientConnectionManager
from titan.debug.debugger import Debugger


class TCPGateway:
    def __init__(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((Config.get("host"), Config.get("port")))
        self._connection_manager = ClientConnectionManager()

        self._listen_task = None
        self._running = False

    async def start(self) -> None:
        self._socket.listen(Config.get("maxConnections", 100))
        self._socket.setblocking(False)

        Debugger.print(
            f"[TCPGateway.start] Server is listeting on {self._socket.getsockname()})\nPress Ctrl+C to stop it"
        )

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

    async def stop(self):
        self._running = False
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass
            self._listen_task = None
        self._socket.close()
        Debugger.print("[TCPGateway.stop] Server stopped")
