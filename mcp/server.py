from mcp.server.fastmcp import FastMCP
import datetime
import json

from keys_generator import generate_raw_keys
import idm

mcp = FastMCP(name='Toolbox')

DID = None

def get_did():
    public_key, secret_key = generate_raw_keys()
    data = {
        'type': 'toolbox',
        'pk': public_key,
        'pktype': 'ed25519',
    }
    global DID
    DID = idm.get_did(data)


@mcp.tool()
def _verify_vc(vc_str: str):
    vc = json.loads(vc_str)
    
    vc_exists = idm.verify_vc(vc)
    if not vc_exists:
        return 'failure'
    
    if vc['credentialSubject']['claim']['service'] == 'callTools':
        return 'success'
    return 'failure'


# AI Tools
@mcp.tool()
def get_current_date():
    """
    Get today's date. Get the current date.

    Return:
        str: The current local date in "YYYY-MM-DD" (YEAR-MONTH-DATE) format.
    """
    current_date = datetime.date.today()
    return str(current_date)

@mcp.tool()
def get_current_time():
    """
    Get the current time.

    Return:
        str: The current local date "%H: %M:%S" (HOURS :MINUTES: SECONDS) format.
    """
    current_time = datetime.datetime.now()
    return current_time.strftime("%H;%M:%S")


if __name__ == "__main__":
    # Request for server identity from IDM
    get_did()
    print(DID)

    # Start MCP Server
    print('Running server with stdio transport')
    mcp.run(transport='stdio')