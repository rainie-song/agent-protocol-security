from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import asyncio
import json
from typing import Optional
from contextlib import AsyncExitStack

from keys_generator import generate_raw_keys
import idm

class MCP_Client:
    def __init__(self):
        # Initialise session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.model = None

        # Security
        self.vc = None
        self.did = None
        self.secret_key = None
        self.public_key = None

        self.get_did()
        self.get_vc()

    def get_did(self):
        print('Generating keys...')
        self.public_key, self.secret_key = generate_raw_keys()
        data = {
            'type': 'AIagent',
            'pk': self.public_key,
            'pktype': 'ed25519',
            'description': 'AIassistant',
            'protocol': 'MCP',
            'transparency': '6GPDL'
        }
        print('Getting DID...')
        self.did = idm.get_did(data)
        print(self.did)

    def get_vc(self):
        print('\nGetting VC...')
        id = self.did['id']
        data = {
            'subjectID': id,
            'content': 'callTools',
            'keyType': 'Ed25519',
            'signType': 'asy',
            'usage': 'authorization'
        }

        self.vc = idm.get_vc(data)
        print(self.vc)

    async def connect_to_server(self, server_script_path: str):
        print('\nConnecting to MCP Server...')
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

    async def verify_vc(self):
        print('\nVerifying VC...')

        args = {
            "vc_str": json.dumps(self.vc)
        }

        result = await self.session.call_tool(
            "_verify_vc",
            arguments=args
        )
        print('result:', result.content[0].text)

        if result.content[0].text == 'success':
            print('Authorised!')
            authorised = True
        else:
            print('Unauthorised!')
            authorised = False

        return authorised

    async def process_message(self):
        authorised = await self.verify_vc()
        if not authorised:
            print('Process message: unauthorised')
            return False
        # Process message will simulate making a tool call after receiving a message that requires tool calling
        print('\nCalling get_current_time tool')
        result = await self.session.call_tool('get_current_time', arguments=None)
        print('result:', result.content[0].text)

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    server_script_path = './mcp/server.py'

    client = MCP_Client()

    try:
        await client.connect_to_server(server_script_path)
        await client.process_message()
    finally:
        await client.cleanup()
    
if __name__ == '__main__':
    asyncio.run(main())