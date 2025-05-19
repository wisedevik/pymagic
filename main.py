import asyncio
from server.Debug.network.tcp.tcp_gateway import TCPGateway
from server.Debug.server_debugger import ServerDebugger
from titan.debug.debugger import Debugger


async def main():
    Debugger.set_listener(ServerDebugger("server_log.txt"))

    gateway = TCPGateway()
    await gateway.start()
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
