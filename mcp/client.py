from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import asyncio
from typing import Optional
from contextlib import AsyncExitStack

class MCP_Client:
    def __init__(self):
        # Initialise session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.model = None

    async def connect_to_server(self, server_script_path: str):
        command = 'python'

        server_params = StdioServerParameters(
            command = command,
            args = [server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        # List available tools
        toolbox = await self.session.list_tools()
        tools = toolbox.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    server_script_path = './mcp/server.py'

    client = MCP_Client()
    try:
        await client.connect_to_server(server_script_path)
    finally:
        await client.cleanup()
    
if __name__ == '__main__':
    asyncio.run(main())