from typing import Tuple
import socket
import asyncio

from server.network.connection.client_connection import ClientConnection
from titan.debug.debugger import Debugger

class ClientConnectionManager:
    def __init__(self) -> None:
        pass

    def on_connect(self, client_socket: socket.socket, addr: Tuple[str, int]):
        Debugger.print(f"[ClientConnectionManager.on_connect] New connection from {addr}");
        asyncio.create_task(self.run_session_async(client_socket))

    async def run_session_async(self, client_socket: socket.socket):
        session = ClientConnection(client_socket)

        try:
            await session.receive()
        except asyncio.CancelledError:
            pass
        except Exception as ex:
            Debugger.error(f"Unhandled exception in session: {ex}")
        finally:
            Debugger.warning("[ClientConnectionManager.run_session_async] User has disconnected")
            client_socket.close()
