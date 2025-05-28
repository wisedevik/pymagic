import asyncio
from logic.messages.logic_magic_message_factory import LogicMagicMessageFactory
from logic.messages.message_registry import auto_import_messages
from server.network.tcp.tcp_gateway import TCPGateway
from server.debug.server_debugger import ServerDebugger
from server.resources.resource_manager import ResourceManager
from titan.debug.debugger import Debugger
import os
import json
import sys
import pathlib

from logic.messages.message_registry import auto_import_messages

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

async def main():
    Debugger.set_listener(ServerDebugger("server_log.txt"))
    Debugger.print(f"Working Directory: {os.getcwd()}")

    ResourceManager.load_game_resources()

    auto_import_messages()

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
