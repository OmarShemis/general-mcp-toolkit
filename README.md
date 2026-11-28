# General MCP Server

A Python MCP server with 27 tools for workspace files, PDF extraction, web
search, webpage reading, command execution, and Windows desktop automation.
FastMCP Code Mode exposes these capabilities through on-demand discovery and
sandboxed Python orchestration rather than loading every tool schema upfront.

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

## Code Mode

Code Mode is enabled by default using FastMCP's experimental `CodeMode`
transform. `requirements.txt` includes the `fastmcp[code-mode]` extra, which
installs the Monty sandbox runtime. Reinstall requirements and restart the
server after upgrading an existing installation.

Clients see three meta-tools instead of the original tool catalog:

1. `search` discovers tools by keyword.
2. `get_schema` provides the selected tools' parameters and return shapes.
3. `execute` runs Python that composes calls to the discovered tools.

For example, search for `read_file`, inspect its schema, then pass this code
to `execute` to read two workspace files and return only their lengths:

```python
first = await call_tool("read_file", {"file_path": "first.txt"})
second = await call_tool("read_file", {"file_path": "second.txt"})
return {"first_chars": len(first["result"]), "second_chars": len(second["result"])}
```

Create these sample files inside `MCP_WORKSPACE` first. `read_file` returns its
text in the structured `result` field; `get_schema` describes this shape.
Tool results remain
inside the code block until returned. Mounted desktop tools are discoverable
through the same layer; inspect their actual names and schemas before calling.
The transform uses its default limit of 50 tool calls per execution.

The Python orchestration runs in a sandbox, but the underlying tools retain
their original server permissions: `run_command` can execute programs and
desktop tools can operate the computer. Code Mode is not an authorization
boundary or a replacement for authentication and trusted-client access.
See the [FastMCP Code Mode documentation](https://gofastmcp.com/docs/servers/transforms/code-mode).

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
