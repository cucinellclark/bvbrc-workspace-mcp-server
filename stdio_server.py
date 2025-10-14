from fastmcp import FastMCP
from json_rpc import JsonRpcCaller
from workspace_tools import register_workspace_tools
import json
import sys
from typing import Any, List

with open("config.json", "r") as f:
    config = json.load(f)

workspace_api_url = config["workspace-url"]

# Initialize the JSON-RPC caller
api = JsonRpcCaller(workspace_api_url)

# Create FastMCP server
mcp = FastMCP("BVBRC Workspace MCP Server")

# Register workspace tools
register_workspace_tools(mcp, api)

# Add health check tool
@mcp.tool()
def health_check() -> str:
    """Health check endpoint"""
    return '{"status": "healthy", "service": "bvbrc-workspace-mcp"}'

def main() -> int:
    print("Starting BVBRC Workspace MCP FastMCP STDIO Server...", file=sys.stderr)
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("Server stopped.", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    main()
