
from fastmcp import FastMCP
from workspace_functions import workspace_ls, workspace_get_file_metadata, workspace_download_file, workspace_upload, workspace_search
from json_rpc import JsonRpcCaller
from token_provider import TokenProvider
from typing import List, Optional

def register_workspace_tools(mcp: FastMCP, api: JsonRpcCaller, token_provider: TokenProvider):
    """Register workspace tools with the FastMCP server"""
    
    @mcp.tool()
    def workspace_ls_tool(token: Optional[str] = None, paths: List[str] = None) -> str:
        """List the contents of the workspace.
        
        Args:
            token: Authentication token (optional - will use default if not provided)
            paths: Optional list of paths to list. If empty or None, lists root workspace.
        
        Returns:
            String representation of workspace contents.
        """
        if paths is None:
            paths = []
        
        # Get the appropriate token
        auth_token = token_provider.get_token(token)
        if not auth_token:
            return "Error: No authentication token available"
        
        print(f"paths: {paths}")
        print(f"token: {auth_token}")
        result = workspace_ls(api, paths, auth_token)
        return str(result)

    @mcp.tool()
    def workspace_search_tool(token: Optional[str] = None, search_term: str = None, paths: List[str] = None) -> str:
        """Search the workspace for a given term.
        
        Args:
            token: Authentication token (optional - will use default if not provided)
            search_term: Term to search the workspace for.
            paths: Optional list of paths to search. If empty or None, searches root workspace.
        """
        if not search_term:
            return "Error: search_term parameter is required"
        
        # Get the appropriate token
        auth_token = token_provider.get_token(token)
        if not auth_token:
            return "Error: No authentication token available"
        
        result = workspace_search(api, paths, search_term, auth_token)
        return str(result)

    @mcp.tool()
    def workspace_get_file_metadata_tool(token: Optional[str] = None, path: str = None) -> str:
        """Get the metadata of a file from the workspace. 
        
        Args:
            token: Authentication token (optional - will use default if not provided)
            path: Path to the file to get.
        """
        if not path:
            return "Error: path parameter is required"
        
        # Get the appropriate token
        auth_token = token_provider.get_token(token)
        if not auth_token:
            return "Error: No authentication token available"
        
        result = workspace_get_file_metadata(api, path, auth_token)
        return str(result)

    @mcp.tool()
    def workspace_download_file_tool(token: Optional[str] = None, path: str = None, output_file: str = None) -> str:
        """Download a file from the workspace.
        
        Args:
            token: Authentication token (optional - will use default if not provided)
            path: Path to the file to download.
            output_file: Name and path of the file to save the downloaded content to.
        """
        if not path:
            return "Error: path parameter is required"
        
        # Get the appropriate token
        auth_token = token_provider.get_token(token)
        if not auth_token:
            return "Error: No authentication token available"
        
        result = workspace_download_file(api, path, auth_token, output_file)
        return str(result)

    @mcp.tool()
    def workspace_upload(token: Optional[str] = None, filename: str = None) -> str:
        """Create an upload URL for a file in the workspace.
        
        Args:
            token: Authentication token (optional - will use default if not provided)
            filename: Name of the file to create upload URL for.
        """
        if not filename:
            return "Error: filename parameter is required"
        
        # Get the appropriate token
        auth_token = token_provider.get_token(token)
        if not auth_token:
            return "Error: No authentication token available"
        
        result = workspace_upload(api, filename, auth_token)
        return str(result)
