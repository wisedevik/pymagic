import asyncio

from server.config.configuration import Configuration
from server.database.base import init_db
from server.network.tcp.tcp_gateway import TCPGateway
from server.debug.server_debugger import ServerDebugger
from server.resources.resource_manager import ResourceManager
from titan.debug.debugger import Debugger

from pyfiglet import figlet_format


async def main():
    print(
        figlet_format(
            Configuration.console.figlet_text, font=Configuration.console.figlet_font
        ),
        end="\n\n",
    )

    Debugger.set_listener(ServerDebugger("server_log.txt"))

    ResourceManager.load_game_resources()
    ResourceManager.load_starting_home_json()

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
