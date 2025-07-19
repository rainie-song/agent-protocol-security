from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import mcp.types as types

async def connect_to_server():
    command = 'python'
    server_path = 'server.py'

    server_params = StdioServerParameters(
        command = command,
        args = [server_path],
        env=None
    )

    async with stdio_client(server)