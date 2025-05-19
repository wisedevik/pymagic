import asyncio
from server.network.tcp.tcp_gateway import TCPGateway
from server.debug.server_debugger import ServerDebugger
from titan.debug.debugger import Debugger


async def main():
    Debugger.set_listener(ServerDebugger("server_log.txt"))

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
