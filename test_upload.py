#!/usr/bin/env python3
"""
Test script for BVBRC Workspace MCP Server upload functionality.
This script loads configuration from config.json and tests the workspace upload function.
"""

import json
import os
import sys
import requests
from workspace_functions import workspace_upload
from json_rpc import JsonRpcCaller

def load_config():
    """Load configuration from config.json file."""
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("Error: config.json file not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config.json: {e}", file=sys.stderr)
        sys.exit(1)

def test_workspace_upload():
    """Test the workspace upload function."""
    print("Loading configuration from config.json...")
    config = load_config()
    
    # Set environment variables from config
    workspace_url = config["workspace-url"]
    token = config["token"]
    
    print(f"Workspace URL: {workspace_url}")
    print(f"Token: {token[:50]}...")  # Show only first 50 chars of token for security
    
    # Initialize the JSON-RPC caller
    api = JsonRpcCaller(workspace_url)
    
    # Test file to upload
    test_filename = "test_upload.txt"
    
    print(f"\nTesting workspace upload with file: {test_filename}")
    print("=" * 50)
    
    try:
        # Call the workspace_upload function
        result = workspace_upload(api, test_filename, token)
        
        print("Upload result:")
        print(json.dumps(result, indent=2))
        
        # Check if the result contains upload URL information
        if isinstance(result, list) and len(result) > 0:
            if "Error" in str(result[0]):
                print(f"\n❌ Upload failed: {result[0]}")
                return False
            else:
                print(f"\n✅ Upload URL created successfully!")
                return True
        else:
            print(f"\n✅ Upload completed successfully!")
            return True
            
    except Exception as e:
        print(f"\n❌ Upload failed with exception: {e}")
        return False
    finally:
        # Clean up the API connection
        api.close()

def main():
    """Main test function."""
    print("BVBRC Workspace MCP Server - Upload Test")
    print("=" * 50)
    
    # Check if test file exists
    if not os.path.exists("test_upload.txt"):
        print("❌ Error: test_upload.txt file not found")
        print("Please ensure test_upload.txt exists in the current directory")
        sys.exit(1)
    
    # Run the test
    success = test_workspace_upload()
    
    if success:
        print("\n🎉 Test completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
