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
        self._reader = reader
        self._writer = writer
        self._messaging = Messaging(reader, writer, MessageManager(self))
        self._buffer = bytearray(8192)
        self.game_mode = GameMode()

    def get_game_mode(self) -> GameMode:
        return self.game_mode

    async def receive(self):
        try:
            offset = 0
            while True:
                data = await self._reader.read(4096)
                if not data:
                    break

                self._buffer[offset : offset + len(data)] = data
                offset += len(data)

                processed_offset = 0
                while True:
                    consumed = await self._messaging.on_receive(
                        self._buffer[processed_offset:offset], offset - processed_offset
                    )
                    if consumed == 0:
                        break
                    processed_offset += consumed

                if processed_offset > 0:
                    self._buffer[: offset - processed_offset] = self._buffer[
                        processed_offset:offset
                    ]
                    offset -= processed_offset

        except asyncio.CancelledError:
            pass
        except Exception as ex:
            Debugger.error(f"Unhandled exception in session: {ex}")

    async def send_message(self, message: PiranhaMessage):
        await self._messaging.send(message)
