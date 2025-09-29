# BV-BRC Workspace MCP Server

A Model Context Protocol (MCP) server that provides access to BV-BRC (Bacterial and Viral Bioinformatics Resource Center) workspace services.

## Features

- List workspace contents and directories
- Get file metadata from the workspace
- Download files from the workspace
- Access BV-BRC workspace through convenient MCP tools

## Installation

### Prerequisites

- Python >= 3.10
- pip

### Install Required Dependencies

0. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install This MCP Server

```bash
git clone https://github.com/cucinellclark/bvbrc-workspace-mcp.git
cd bvbrc-workspace-mcp
pip install -r requirements.txt
```

## Configuration

The server uses a `config.json` file for configuration:

```json
{
    "workspace-url": "https://p3.theseed.org/services/Workspace",
    "port": 8057,
    "token": "<bvbrc_token>"
}
```

## Usage

Run the MCP server:

```bash
python server.py
```

The server will start on port 8057 (configurable in `config.json`).
