# agent-protocol-security
In recent years, AI agents have witnessed remarkable progress and are increasingly recognized as a pivotal force in various fields. Regarding agent protocols, they play a crucial role in enabling seamless communication between agents, external tools, and data sources. However, with the development of AI agents and their protocols, security has become a pressing concern.
This repository is used for code collection of IETF Hackathon. In this hackathon we aim to validate the security design (e.g. identity, authentication, authiorization) for agent protocols, including agent-to-other protocols (e.g. MCP), or agent-to-agent protocols (e.g. A2A).

# IETF 123 Hackathon on Agent Protocol Security
## Reference links
- https://modelcontextprotocol.io/introduction
- https://github.com/modelcontextprotocol
- https://github.com/modelcontextprotocol/python-sdk

## Install Python (3.10.2)

## Create Python Virtual Environment

Create Python virtual environment inside the project. 
1. Run Command Prompt and navigate to the project location. 

        $ cd /path/to/project_folder

2. Then create a python virtual environment in the folder.

        $ python -m venv .venv

3. Activate python virtual environment.

        $ .venv\Scripts\activate

## Installing dependencies

        $ pip install -r requirements.txt

## Run client.py in mcp folder

        $ python mcp/client.py


## Additional information:

### Build MCP Server

Simple MCP server with tools:  
https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#tools

Additional notes:
- Transport Layer: stdio
- Add a code line to run the server using stdio transport layer

### MCP Client

Simple MCP client:  
https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients

Additional notes:
- Transport Layer: stdio
- add command line to run the simple MCP server
- Integrate local LLM into client
