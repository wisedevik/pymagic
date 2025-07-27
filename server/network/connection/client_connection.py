import asyncio

from server.mode.game_mode import GameMode
from server.network.protocol import MessageManager
from server.network.protocol import Messaging
from titan.debug.debugger import Debugger
from titan.message.piranha_message import PiranhaMessage


class ClientConnection:
    def __init__(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        self.reader = reader
        self.writer = writer
        self.messaging = Messaging(reader, writer)
        self.message_manager = MessageManager(self)
        self.buffer = bytearray()
        self.game_mode = GameMode()

    def get_game_mode(self) -> GameMode:
        return self.game_mode

    async def receive(self):
        try:
            while data := await self.reader.read(4096):
                self.buffer.extend(data)

                while self.buffer:
                    consumed = await self.messaging.on_receive(
                        memoryview(self.buffer), len(self.buffer)
                    )
                    if not consumed:
                        break

                    message = await self.messaging.next_message()
                    await self.message_manager.receive_message(message)
                    del self.buffer[:consumed]

        except asyncio.CancelledError:
            pass
        except Exception as ex:
            Debugger.error(f"Unhandled exception in session: {ex}")

    async def send_message(self, message: PiranhaMessage):
        await self.messaging.send(message)
