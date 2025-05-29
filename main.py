import asyncio
from config import Config
from logic.messages.logic_magic_message_factory import LogicMagicMessageFactory
from server.network.tcp.tcp_gateway import TCPGateway
from server.debug.server_debugger import ServerDebugger
from server.resources.resource_manager import ResourceManager
from titan.debug.debugger import Debugger
import os
import json
import sys
import pathlib


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


async def main():
    Debugger.set_listener(ServerDebugger("server_log.txt"))
    Debugger.print(f"Working Directory: {os.getcwd()}")

    ResourceManager.load_game_resources()

    Config.load()

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
