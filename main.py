import asyncio

from server.config import Configuration
from server.network.tcp.tcp_gateway import TCPGateway
from server.debug.server_debugger import ServerDebugger
from server.resources import ResourceManager
from titan.debug.debugger import Debugger

from pyfiglet import figlet_format
from server.database import init_db
import logging

from titan.math.logic_random import LogicRandom
from titan.math.logic_vector2 import LogicVector2


async def main():
    print(
        figlet_format(
            Configuration.console.figlet_text, font=Configuration.console.figlet_font
        ),
        end="\n\n",
    )

    Debugger.set_listener(ServerDebugger("server_log.txt"))

    ResourceManager.load_game_resources()

    await init_db()

    gateway = TCPGateway()
    await gateway.start()

    try:
        await asyncio.Future()
    finally:
        await gateway.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
