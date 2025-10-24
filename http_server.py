from fastmcp import FastMCP
from json_rpc import JsonRpcCaller
from workspace_tools import register_workspace_tools
from token_provider import TokenProvider
import json
import sys
from typing import Any, List

with open("config.json", "r") as f:
    config = json.load(f)

workspace_api_url = config["workspace-url"]
port = config.get("port", 5000)
mcp_url = config.get("mcp_url", "127.0.0.1")

# Initialize token provider for HTTP mode
token_provider = TokenProvider(mode="http")

# Initialize the JSON-RPC caller
api = JsonRpcCaller(workspace_api_url)

# Create FastMCP server
mcp = FastMCP("BVBRC Workspace MCP Server")

# Register workspace tools with token provider
register_workspace_tools(mcp, api, token_provider)

# Add health check tool
@mcp.tool()
def health_check() -> str:
    """Health check endpoint"""
    return '{"status": "healthy", "service": "bvbrc-workspace-mcp"}'

@mcp.custom_route("/.well-known/openid-configuration", methods=["GET"])
def openid_configuration() -> str:
    """
    Serves the OIDC discovery document that ChatGPT expects.
    """
    config = {
            "issuer": "https://www.bv-brc.org",
            "authorization_endpoint": "https://dev-6.bv-brc.org/oauth2/authorize",
            "token_endpoint": "https://dev-6.bv-brc.org/oauth2/token",
            "registration_endpoint": "https://dev-6.bv-brc.org/oauth2/register", # 1
            "response_types_supported": ["code"],
            "grant_types_supported": ["authorization_code"],
            "token_endpoint_auth_methods_supported": ["none", "client_secret_post"],
            "code_challenge_methods_supported": ["S256"],
            "scopes_supported": ["profile", "token"],
            "claims_supported": ["sub", "api_token"]
    }
    return json.dumps(config)

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
