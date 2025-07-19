from mcp.server.fastmcp import FastMCP
import datetime

mcp = FastMCP(name='Toolbox')

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
    # Start MCP Server
    print('Running server with stdio transport')
    mcp.run(transport='stdio')