"""Use CursorTouch/Windows-MCP v0.9.0 directly inside this MCP server.

Source: https://github.com/CursorTouch/Windows-MCP
The dependency is pinned because its server factory is an internal API.
"""

import os

from fastmcp import FastMCP
from windows_mcp.__main__ import _apply_tool_filter, _build_mcp
from ._desktop_reliability import DesktopReliability, wait_seconds


def create_computer_use() -> FastMCP:
    """Register the original Windows-MCP desktop tools, including its lifecycle."""
    os.environ.setdefault("ANONYMIZED_TELEMETRY", "false")
    server = _build_mcp()
    _apply_tool_filter(server, explicit_tools=[
        "Screenshot", "Snapshot", "Click", "Type", "Scroll", "Move",
        "Shortcut", "WaitFor", "App", "Clipboard", "ControlStatus",
    ], exclude_tools=None)
    server.tool(name="Wait")(wait_seconds)
    server.add_middleware(DesktopReliability())
    return server
