import requests
import json
from typing import Any, Dict, Optional


class JsonRpcCaller:
    """A minimal, generic JSON-RPC caller class."""
    
    def __init__(self, workspace_url: str):
        """
        Initialize the JSON-RPC caller with workspace URL and authentication token.
        
        Args:
            workspace_url: The base URL for the workspace API
            token: Authentication token for API calls
        """
        self.workspace_url = workspace_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/jsonrpc+json'
        })
    
    def call(self, method: str, params: Optional[Dict[str, Any]] = None, request_id: int = 1, token: str = None) -> Dict[str, Any]:
        """
        Make a JSON-RPC call to the workspace API.
        
        Args:
            method: The RPC method name to call
            params: Optional parameters for the method
            request_id: Request ID for the JSON-RPC call
            token: Authentication token for API calls
        Returns:
            The response from the API call
            
        Raises:
            requests.RequestException: If the HTTP request fails
            ValueError: If the response contains an error
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": request_id,
            "params": params
        }

        if token:
            self.session.headers.update({
                'Authorization': f'{token}'
            })

        try:
            response = self.session.post(
                self.workspace_url,
                data=json.dumps(payload),
                timeout=30
            )

            response.raise_for_status()
            
            result = response.json()
            
            # Check for JSON-RPC errors
            if "error" in result:
                raise ValueError(f"JSON-RPC error: {result['error']}")
            
            return result.get("result", {})
        
        except Exception as e:
            print(f"error: {e.response.text}")
        except requests.RequestException as e:
            raise requests.RequestException(f"HTTP request failed: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")

    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
