import requests
import json

# Updated endpoints for FastMCP with streaming support
tools_url = "http://127.0.0.1:8057/mcp/tools/list"
call_url = "http://127.0.0.1:8057/mcp/tools/call"

with open("config.json", "r") as f:
    config = json.load(f)

token = config["token"]

if False:
    print('********* listing tools *********')

    url = tools_url

    response = requests.get(url)

    print(response.json())

if False:
    print('********* calling tool: workspace_ls *********')

    url = call_url

    params = {
        "token": token,
        "paths": ['/clark.cucinell@patricbrc.org/home/Feature Groups','/clark.cucinell@patricbrc.org/home/Genome Groups']
    }

    response = requests.post(url, json={"jsonrpc": "2.0", "id": 1, "name": "workspace_ls", "params": params})

    print(response.json())

if False:
    print('********* calling tool: workspace_get_file_metadata *********')

    url = call_url

    params = {
        "token": token,
        "path": "/clark.cucinell@patricbrc.org/home/bvbrc_rnaseq_report_test.html"
    }

    response = requests.post(url, json={"jsonrpc": "2.0", "id": 1, "name": "workspace_get_file_metadata", "params": params})

    print(response.json())

if True:
    print('********* calling tool: workspace_download_file *********')

    url = call_url

    params = {
        "token": token,
        "path": "/clark.cucinell@patricbrc.org/home/bvbrc_rnaseq_report_test.html"
    }

    response = requests.post(url, json={"jsonrpc": "2.0", "id": 1, "name": "workspace_download_file", "params": params})

    print(response.json())