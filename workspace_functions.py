from json_rpc import JsonRpcCaller
from typing import List, Any
import requests
import os

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

def workspace_search(api: JsonRpcCaller, paths: List[str] = None, search_term: str = None, token: str = None) -> str:
    """
    Search the workspace for a given term.
    """
    if not paths:
        user_id = _get_user_id_from_token(token)
        if not user_id:
            return [f"Error searching workspace: unable to derive user id from token"]
        paths = [f"/{user_id}/home"]
    if not search_term:
        return [f"Error searching workspace: search_term parameter is required"]
    
    try:
        result = api.call("Workspace.ls", {
            "recursive": True,
            "excludeDirectories": False,
            "excludeObjects": False,
            "includeSubDirs": True,
            "paths": paths,
            "query": {
                "name": {
                    "$regex": search_term,
                    "$options": "i"
                }
            }
        },1, token)
        return result
    except Exception as e:
        return [f"Error searching workspace: {str(e)}"]

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


def workspace_download_file(api: JsonRpcCaller, path: str, token: str, output_file: str = None) -> str:
    """
    Download a file from the workspace using the JSON-RPC API.
    
    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        path: Path to the file to download
        token: Authentication token for API calls
        output_file: Name and path of the file to save the downloaded content to.
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

        if output_file:
            with open(output_file, 'wb') as file:
                file.write(response.content)
            return f"File downloaded and saved to {output_file}"
        else:
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

def _get_user_id_from_token(token: str) -> str:
    """
    Extract user ID from a BV-BRC/KBase style auth token.
    Returns None if token is None or invalid.
    """
    if not token:
        return None
    try:
        # Token format example: "un=username|..."; take first segment and strip prefix
        return token.split('|')[0].replace('un=','')
    except Exception as e:
        print(f"Error extracting user ID from token: {e}")
        return None

def workspace_upload(api: JsonRpcCaller, filename: str, upload_dir: str = None, token: str = None) -> str:
    """
    Create an upload URL for a file in the workspace using the JSON-RPC API.
    
    Args:
        api: JsonRpcCaller instance configured with workspace URL and token
        filename: Name of the file to create upload URL for
        upload_dir: Directory to upload the file to (defaults to /<user_id>/home)
        token: Authentication token for API calls (required)
    Returns:
        String representation of the upload URL response with parsed metadata
    """
    try:
        
        if not token:
            return {"error": "Authentication token not provided"}

        if not upload_dir:
            user_id = _get_user_id_from_token(token)
            if not user_id:
                return {"error": "Unable to derive user id from token"}
            upload_dir = '/' + user_id + '/home'
        download_url_path = os.path.join(upload_dir,os.path.basename(filename))
        # call format: workspace file location, file type, object metadata, object content
        result = _workspace_create(
            api,
            [[download_url_path, 'unspecified', {}, '']],
            token,
            create_upload_nodes=True,
            overwrite=None
        )
        
        # Parse the result if successful
        if result and len(result) > 0 and len(result[0]) > 0:
            # Extract the metadata array from result[0][0]
            meta_list = result[0][0]
            
            # Convert the array to a structured object
            meta_obj = {
                "id": meta_list[4],
                "path": meta_list[2] + meta_list[0],
                "name": meta_list[0],
                "type": meta_list[1],
                "creation_time": meta_list[3],
                "link_reference": meta_list[11],
                "owner_id": meta_list[5],
                "size": meta_list[6],
                "userMeta": meta_list[7],
                "autoMeta": meta_list[8],
                "user_permission": meta_list[9],
                "global_permission": meta_list[10],
                "timestamp": meta_list[3]  # Keep as string for now, could parse to timestamp if needed
            }

            upload_url = meta_obj["link_reference"]

            msg = {
                "file": os.path.basename(filename),
                "uploadDirectory": upload_dir,
                "url": upload_url
            }
            
            # Upload the file to the upload URL
            print(f"Uploading file to {upload_url}")
            upload_result = _upload_file_to_url(filename, upload_url, token)
            print(f"Upload result: {upload_result}")
            if upload_result.get("success"):
                msg["upload_status"] = "success"
                msg["upload_message"] = upload_result.get("message", "File uploaded successfully")
            else:
                msg["upload_status"] = "failed"
                msg["upload_error"] = upload_result.get("error", "Upload failed")
            
            return msg
        else:
            return {"error": "No valid result returned from workspace API"}
            
    except Exception as e:
        return {"error": f"Error creating upload URL: {str(e)}"}

def _workspace_create(api: JsonRpcCaller, objects: list, token: str, create_upload_nodes: bool = True, overwrite: Any = None):
    """
    Helper to invoke Workspace.create via JSON-RPC.
    """
    try:
        return api.call(
            "Workspace.create",
            {
                "objects": objects,
                "createUploadNodes": create_upload_nodes,
                "overwrite": overwrite
            },
            1,
            token
        )
    except Exception as e:
        return [f"Error creating workspace object: {str(e)}"]

def _upload_file_to_url(filename: str, upload_url: str, token: str) -> dict:
    """
    Upload a file to the specified Shock API URL using binary data.
    
    Args:
        filename: Path to the file to upload
        upload_url: The upload URL from workspace API
        token: Authentication token for API calls
    Returns:
        Dictionary with upload result status and message
    """
    try:
        # Check if file exists
        if not os.path.exists(filename):
            return {"success": False, "error": f"File {filename} does not exist"}
        
        # Read the file content
        with open(filename, 'rb') as file:
            file_content = file.read()
        
        # Set up headers for the Shock API request
        headers = {
            'Authorization': 'OAuth ' + token
        }
        
        # Prepare the file for multipart form data upload
        with open(filename, 'rb') as file:
            files = {
                'upload': (os.path.basename(filename), file, 'application/octet-stream')
            }
            
            # Make the POST request with multipart form data
            response = requests.put(upload_url, files=files, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return {
                "success": True, 
                "message": f"File {filename} uploaded successfully",
                "status_code": response.status_code
            }
        else:
            return {
                "success": False, 
                "error": f"Upload failed with status code {response.status_code}: {response.text}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        return {"success": False, "error": f"Upload failed: {str(e)}"}

def workspace_create_genome_group(api: JsonRpcCaller, genome_group_path: str, genome_id_list: List[str], token: str) -> str:
    """
    Create a genome group in the workspace using the JSON-RPC API.
    """
    genome_group_name = genome_group_path.split('/')[-1]
    try:
        content = {
            'id_list': {
                'genome_id': genome_id_list
            }, 
            'name': genome_group_name
        }
        result = api.call("Workspace.create", {
            "objects": [[genome_group_path, 'genome_group', {}, content]]
        },1, token)
        return result
    except Exception as e:
        return [f"Error creating genome group: {str(e)}"]

def workspace_create_feature_group(api: JsonRpcCaller, feature_group_path: str, feature_id_list: List[str], token: str) -> str:
    """
    Create a feature group in the workspace using the JSON-RPC API.
    """
    feature_group_name = feature_group_path.split('/')[-1]
    try:
        content = {
            'id_list': {
                'feature_id': feature_id_list
            }, 
            'name': feature_group_name
        }
        result = api.call("Workspace.create", {
            "objects": [[feature_group_path, 'feature_group', {}, content]]
        },1, token)
        return result
    except Exception as e:
        return [f"Error creating feature group: {str(e)}"]