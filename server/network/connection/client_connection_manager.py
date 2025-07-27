import asyncio
from typing import Dict, Tuple

from server.network.connection import ClientConnection
from titan.debug.debugger import Debugger


class ClientConnectionManager:
    async def on_connect(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        addr = writer.get_extra_info("peername")
        Debugger.print(f"New connection from {addr}")

        session = ClientConnection(reader, writer)
        try:
            await session.receive()
        finally:
            Debugger.warning("User has disconnected")
