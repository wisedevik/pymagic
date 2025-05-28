import asyncio
from typing import cast
from logic.data.data_objects.logic_building_data import LogicBuildingData
from logic.data.tables.logic_data_tables import LogicDataTables
from logic.data.core.logic_data_type import LogicDataType
from server.network.tcp.tcp_gateway import TCPGateway
from server.debug.server_debugger import ServerDebugger
from server.resources.resource_manager import ResourceManager
from titan.debug.debugger import Debugger
import os
import json
from logic.data.data_objects.logic_resource_data import LogicResourceData



def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

async def main():
    Debugger.set_listener(ServerDebugger("server_log.txt"))
    Debugger.print(f"Working Directory: {os.getcwd()}")

    ResourceManager.load_game_resources()

    config = load_config()
    gateway = TCPGateway(config)
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
