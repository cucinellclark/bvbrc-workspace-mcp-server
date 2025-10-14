
from fastmcp import FastMCP
from workspace_functions import workspace_ls, workspace_get_file_metadata, workspace_download_file, workspace_upload
from json_rpc import JsonRpcCaller
from typing import List

def register_workspace_tools(mcp: FastMCP, api: JsonRpcCaller):
    """Register workspace tools with the FastMCP server"""
    
    @mcp.tool()
    def workspace_ls_tool(token: str, paths: List[str] = None) -> str:
        """List the contents of the workspace.
        
        Args:
            token: Authentication token
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

    @mcp.tool()
    def workspace_get_file_metadata_tool(token: str, path: str) -> str:
        """Get the metadata of a file from the workspace. 
        
        Args:
            token: Authentication token
            path: Path to the file to get.
        """
        result = workspace_get_file_metadata(api, path, token)
        return str(result)

    @mcp.tool()
    def workspace_download_file_tool(token: str, path: str) -> str:
        """Download a file from the workspace.
        
        Args:
            token: Authentication token
            path: Path to the file to download.
        """
        result = workspace_download_file(api, path, token)
        return str(result)

    @mcp.tool()
    def workspace_upload(token: str, filename: str) -> str:
        """Create an upload URL for a file in the workspace.
        
        Args:
            filename: Name of the file to create upload URL for.
        """
        result = workspace_upload(api, filename, token)
        return str(result)
