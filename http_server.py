from fastmcp import FastMCP
from json_rpc import JsonRpcCaller
from workspace_tools import register_workspace_tools
from token_provider import TokenProvider
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
import json
import sys
from typing import Any, List
from auth import (
    openid_configuration, 
    oauth2_register, 
    oauth2_authorize, 
    oauth2_login, 
    oauth2_token
)

with open("config.json", "r") as f:
    config = json.load(f)

workspace_api_url = config["workspace-url"]
authentication_url = config["authentication_url"]
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
async def openid_configuration_route(request) -> JSONResponse:
    """
    Serves the OIDC discovery document that ChatGPT expects.
    """
    return openid_configuration(request)

@mcp.custom_route("/oauth2/register", methods=["POST"])
async def oauth2_register_route(request) -> JSONResponse:
    """
    Registers a new client with the OAuth2 server.
    Implements RFC 7591 OAuth 2.0 Dynamic Client Registration.
    """
    return await oauth2_register(request)

@mcp.custom_route("/oauth2/authorize", methods=["GET"])
async def oauth2_authorize_route(request):
    """
    Authorization endpoint - displays login page for user authentication.
    This is where ChatGPT redirects the user to log in.
    """
    return await oauth2_authorize(request, authentication_url)

@mcp.custom_route("/oauth2/login", methods=["POST"])
async def oauth2_login_route(request):
    """
    Handles the login form submission.
    Authenticates the user and generates an authorization code.
    Redirects back to ChatGPT's callback URL with the code.
    """
    return await oauth2_login(request, authentication_url)

@mcp.custom_route("/oauth2/token", methods=["POST"])
async def oauth2_token_route(request):
    """
    Handles the token request.
    Exchanges an authorization code for an access token.
    Retrieves the stored user token using the authorization code.
    """
    return await oauth2_token(request)

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
