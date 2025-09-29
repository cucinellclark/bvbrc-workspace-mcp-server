from json_rpc import JsonRpcCaller
from typing import List, Any
import requests


def workspace_ls(api: JsonRpcCaller, paths: List[str], token: str) -> List[str]:
    """
    List workspace contents using the JSON-RPC API.
    
    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        paths: List of paths to list
        token: Authentication token for API calls
    Returns:
        List of workspace items
    """
    try:
        result = api.call("Workspace.ls", {
            "Recursive": False,
            "includeSubDirs": False,
            "paths": paths
        },1, token)
        return result
    except Exception as e:
        return [f"Error listing workspace: {str(e)}"]

def workspace_get_file_metadata(api: JsonRpcCaller, path: str, token: str) -> str:
    """
    Get the metadata of a file from the workspace using the JSON-RPC API.
    
    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        path: Path to the file to get the metadata of
        token: Authentication token for API calls
    Returns:
        String representation of the file metadata
    """
    try:
        result = api.call("Workspace.get", {
            "objects": [path],
            "metadata_only": True
        },1, token)
        return result
    except Exception as e:
        return [f"Error getting file metadata: {str(e)}"]


def workspace_download_file(api: JsonRpcCaller, path: str, token: str) -> str:
    """
    Download a file from the workspace using the JSON-RPC API.
    
    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        path: Path to the file to download
        token: Authentication token for API calls
    Returns:
        String representation of the downloaded file
    """
    try:
        download_url_obj = _get_download_url(api, path, token)
        download_url = download_url_obj[0][0]
        
        headers = {
            "Authorization": token
        }
        
        response = requests.get(download_url, headers=headers)
        response.raise_for_status()
        
        return response.content
    except Exception as e:
        return [f"Error downloading file: {str(e)}"]

def _get_download_url(api: JsonRpcCaller, path: str, token: str) -> str:
    """
    Get the download URL of a file from the workspace using the JSON-RPC API.
    
    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        path: Path to the file to get the download URL of
        token: Authentication token for API calls
    Returns:
        String representation of the download URL
    """
    try:
        result = api.call("Workspace.get_download_url", {
            "objects": [path],
        },1, token)
        return result
    except Exception as e:
        return [f"Error getting download URL: {str(e)}"]
