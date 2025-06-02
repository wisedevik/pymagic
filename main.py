import asyncio
from asyncio.tasks import Task

from server.network.tcp.tcp_gateway import TCPGateway
from server.debug.server_debugger import ServerDebugger
from server.resources import ResourceManager
from titan.debug.debugger import Debugger
from logic.data.core.logic_data_type import LogicDataType

from pyfiglet import figlet_format


async def main():
    print(figlet_format("PyMagic", font="slant"), end="\n\n")

    Debugger.set_listener(ServerDebugger("server_log.txt"))

    ResourceManager.load_game_resources()

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
