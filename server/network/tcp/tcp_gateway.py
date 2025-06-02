import asyncio
from typing import Optional

from titan.config import Configuration
from server.network.connection import ClientConnectionManager
from titan.debug.debugger import Debugger


class TCPGateway:
    def __init__(self) -> None:
        self._server: Optional[asyncio.Server] = None
        self._connection_manager = ClientConnectionManager()

    async def start(self) -> None:
        self._server = await asyncio.start_server(
            self._connection_manager.on_connect,
            host=Configuration.server.host,
            port=Configuration.server.port,
            limit=Configuration.server.max_connections,
        )

        Debugger.print(
            f"Server is listening on {self._server.sockets[0].getsockname()})"
        )

    async def stop(self):
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            Debugger.print("Server stopped")
