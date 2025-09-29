from flask import Flask
from flaskmcp import create_app, tool, register_resource, register_prompt
from workspace_functions import workspace_ls, workspace_get_file_metadata, workspace_download_file
from json_rpc import JsonRpcCaller
import json
import sys
from typing import Any, List

with open("config.json", "r") as f:
    config = json.load(f)

workspace_api_url = config["workspace-url"]
port = config.get("port", 5000)

# Initialize the JSON-RPC caller
api = JsonRpcCaller(workspace_api_url)

# Create Flask app and MCP server
app = create_app({'DEBUG': True})

@tool(name="workspace_ls", description="List the contents of the workspace. Parameters: paths: List[str] - list of workspace paths to list (empty list for root workspace)")
def workspace_ls_tool(token: str, paths: List[str] = None) -> str:
    """List the contents of the workspace.
    
    Args:
        paths: Optional list of paths to list. If empty or None, lists root workspace.
    
    Returns:
        String representation of workspace contents.
    """
    if paths is None:
        paths = []
    print(f"paths: {paths}")
    print(f"token: {token}")
    result = workspace_ls(api, paths, token)
    return str(result)

@tool(name="workspace_get_file_metadata", description="Get the metadata of a file from the workspace. Parameters: path: str - full workspace path to the file")
def workspace_get_file_metadata_tool(token: str, path: str) -> str:
    """Get the metadata of a file from the workspace. 
    
    Args:
        path: Path to the file to get.
    """
    result = workspace_get_file_metadata(api, path, token)
    return str(result)

@tool(name="workspace_download_file", description="Download a file from the workspace. Parameters: path: str - full workspace path to the file to download")
def workspace_download_file_tool(token: str, path: str) -> str:
    """Download a file from the workspace.
    
    Args:
        path: Path to the file to download.
    """
    result = workspace_download_file(api, path, token)
    return str(result)

# Optional: Add a health check route
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    from flask import jsonify
    return jsonify({"status": "healthy", "service": "bvbrc-workspace-mcp"})

def main() -> int:
    print(f"Starting BVBRC Workspace MCP Flask Server on port {port}...", file=sys.stderr)
    try:
        app.run(host="127.0.0.1", port=port, debug=True)
    except KeyboardInterrupt:
        print("Server stopped.", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    main()
