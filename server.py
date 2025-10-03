from fastmcp import FastMCP
from workspace_functions import workspace_ls, workspace_get_file_metadata, workspace_download_file, workspace_upload
from json_rpc import JsonRpcCaller
import json
import sys
import os
from typing import Any, List

# Get configuration from environment variables
workspace_api_url = os.getenv("WORKSPACE_API_URL")
if not workspace_api_url:
    print("Error: WORKSPACE_API_URL environment variable not set", file=sys.stderr)
    sys.exit(1)

# Initialize the JSON-RPC caller
api = JsonRpcCaller(workspace_api_url)

# Create FastMCP server
mcp = FastMCP("BVBRC Workspace MCP Server")

@mcp.tool()
def workspace_ls(paths: List[str] = None) -> str:
    """List the contents of the workspace.
    
    Args:
        paths: Optional list of paths to list. If empty or None, lists root workspace.
    
    Returns:
        String representation of workspace contents.
    """
    token = os.getenv("WORKSPACE_TOKEN")
    if not token:
        return "Error: WORKSPACE_TOKEN environment variable not set"
    
    if paths is None:
        paths = []
    print(f"paths: {paths}")
    result = workspace_ls(api, paths, token)
    return str(result)

@mcp.tool()
def workspace_get_file_metadata(path: str) -> str:
    """Get the metadata of a file from the workspace. 
    
    Args:
        path: Path to the file to get.
    """
    token = os.getenv("WORKSPACE_TOKEN")
    if not token:
        return "Error: WORKSPACE_TOKEN environment variable not set"
    
    result = workspace_get_file_metadata(api, path, token)
    return str(result)

@mcp.tool()
def workspace_download_file(path: str) -> str:
    """Download a file from the workspace.
    
    Args:
        path: Path to the file to download.
    """
    token = os.getenv("WORKSPACE_TOKEN")
    if not token:
        return "Error: WORKSPACE_TOKEN environment variable not set"
    
    result = workspace_download_file(api, path, token)
    return str(result)

@mcp.tool()
def workspace_upload(filename: str) -> str:
    """Create an upload URL for a file in the workspace.
    
    Args:
        filename: Name of the file to create upload URL for.
    """
    token = os.getenv("WORKSPACE_TOKEN")
    if not token:
        return "Error: WORKSPACE_TOKEN environment variable not set"
    
    result = workspace_upload(api, filename, token)
    return str(result)

def main() -> int:
    print("Starting BVBRC Workspace MCP Server...", file=sys.stderr)
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("Server stopped.", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    main()
