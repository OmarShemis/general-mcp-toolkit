# General MCP Server

A Python MCP server with 27 tools for workspace files, PDF extraction, web
search, webpage reading, command execution, and Windows desktop automation.

## Requirements

- Windows with an interactive desktop session for desktop automation
- Python 3.14
- Git and uv
- A Tavily API key for web search

## Setup (PowerShell)

```powershell
cd mcp_general
uv venv --python 3.14
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` locally and set `TAVILY_API_KEY`. Then start the server:

```powershell
.\.venv\Scripts\python.exe MCP_Server/server.py
```

The local MCP endpoint is `http://localhost:8000/mcp`.
Restart the server after changing `.env`.

## Connect Codex

```powershell
codex mcp add general-mcp --url http://localhost:8000/mcp
```

## Tests

From `mcp_general`:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Behavior and limitations

- File tools use `MCP_WORKSPACE`, defaulting to `mcp_general`.
- Desktop tools operate on the Windows computer running the server.
- User input can interrupt desktop automation. Inspect the field before
  resuming interrupted typing; do not replay the entire operation.
- PDF extraction reads embedded text, without OCR.
- Commands run with the server user's OS permissions, without a shell.
- The server currently listens on `0.0.0.0` and has no application-level
  authentication configured. Configure authentication before public hosting.
- GitHub stores the source code; it does not run this Windows server.

## Dependencies

Desktop tools use [CursorTouch/Windows-MCP](https://github.com/CursorTouch/Windows-MCP),
pinned to a specific commit in `requirements.txt`. Local reliability adapters
extend the upstream tools without modifying the installed dependency.

Secrets, virtual environments, and local editor files are excluded from Git.
