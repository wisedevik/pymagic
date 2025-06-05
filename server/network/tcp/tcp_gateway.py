import asyncio
from typing import Optional

from server.config import Configuration
from server.network.connection import ClientConnectionManager
from titan.debug.debugger import Debugger


class TCPGateway:
    def __init__(self) -> None:
        self.server: Optional[asyncio.Server] = None
        self.connection_manager = ClientConnectionManager()

    async def start(self) -> None:
        self.server = await asyncio.start_server(
            self.connection_manager.on_connect,
            host=Configuration.server.host,
            port=Configuration.server.port,
            limit=Configuration.server.max_connections,
        )

        Debugger.print(
            f"Server is listening on {self.server.sockets[0].getsockname()})"
        )

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            Debugger.print("Server stopped")
