import os
import json
import sys
from typing import Optional

class TokenProvider:
    """Handles token retrieval for both stdio and HTTP modes"""
    
    def __init__(self, mode: str = "stdio", config_path: str = "config.json"):
        self.mode = mode
        self.config_path = config_path
        self._config_token = None
    
    def get_token(self, provided_token: Optional[str] = None) -> Optional[str]:
        """
        Get token based on mode and provided token.
        
        Args:
            provided_token: Token provided by the tool call (for HTTP mode)
            
        Returns:
            The appropriate token to use
        """
        if provided_token:
            # If token is provided (HTTP mode), use it
            return provided_token
        
        if self.mode == "stdio":
            # STDIO mode: get from environment
            return os.getenv("KB_AUTH_TOKEN")
        else:
            # HTTP mode: get from config
            if self._config_token is None:
                self._load_config_token()
            return self._config_token
    
    def _load_config_token(self):
        """Load token from config file"""
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                self._config_token = config.get("token")
        except Exception as e:
            print(f"Warning: Could not load token from config: {e}", file=sys.stderr)
            self._config_token = None
