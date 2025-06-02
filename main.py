import asyncio
from asyncio.tasks import Task

from logic.avatar.logic_client_avatar import LogicClientAvatar
from logic.data.tables.logic_data_tables import LogicDataTables
from server.network.tcp.tcp_gateway import TCPGateway
from titan.config import Configuration
from server.debug.server_debugger import ServerDebugger
from server.resources.resource_manager import ResourceManager
from titan.debug.debugger import Debugger


async def main():
    Debugger.set_listener(ServerDebugger("server_log.txt"))

    ResourceManager.load_game_resources()

    table = LogicDataTables.get_table(LogicDataType.MISSION)
    print(table.get_item_count())

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
