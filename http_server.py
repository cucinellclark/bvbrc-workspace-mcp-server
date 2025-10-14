from fastmcp import FastMCP
from json_rpc import JsonRpcCaller
from workspace_tools import register_workspace_tools
import json
import sys
from typing import Any, List

with open("config.json", "r") as f:
    config = json.load(f)

workspace_api_url = config["workspace-url"]
port = config.get("port", 5000)
mcp_url = config.get("mcp_url", "127.0.0.1")

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
    print(f"Starting BVBRC Workspace MCP FastMCP HTTP Server on port {port}...", file=sys.stderr)
    try:
        mcp.run(transport="http", host=mcp_url, port=port)
    except KeyboardInterrupt:
        print("Server stopped.", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    main()
