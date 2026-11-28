"""Exercise the server's Code Mode without operating the Windows desktop."""

import importlib.util
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from types import ModuleType
import unittest
from unittest.mock import patch

from fastmcp import Client, FastMCP

SERVER = Path(__file__).resolve().parents[1] / "MCP_Server"
sys.path.insert(0, str(SERVER))


class CodeModeTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.environment = patch.dict(os.environ, MCP_WORKSPACE=self.directory.name)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        # Replace only the desktop provider; file tools and CodeMode are real.
        desktop = FastMCP("Desktop test provider")

        @desktop.tool
        def probe() -> str:
            """Return a test marker without operating the desktop."""
            return "mounted"

        replacement = ModuleType("tools.computer_use")
        replacement.create_computer_use = lambda: desktop
        spec = importlib.util.spec_from_file_location("code_mode_test_server", SERVER / "server.py")
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"tools.computer_use": replacement}):
            spec.loader.exec_module(module)
        self.client = Client(module.mcp)
        await self.client.__aenter__()
        self.addAsyncCleanup(self.client.__aexit__, None, None, None)

    async def test_discovery_and_chained_file_calls(self):
        names = {tool.name for tool in await self.client.list_tools()}
        self.assertEqual(names, {"search", "get_schema", "execute"})
        found = await self.client.call_tool("search", {"query": "read_file"})
        self.assertIn("read_file", str(found.content))
        schema = await self.client.call_tool("get_schema", {"tools": ["read_file"]})
        self.assertIn("file_path", str(schema.content))
        Path(self.directory.name, "first.txt").write_text("hello", encoding="utf-8")
        Path(self.directory.name, "second.txt").write_text("world!", encoding="utf-8")
        result = await self.client.call_tool("execute", {"code": (
            'first = await call_tool("read_file", {"file_path": "first.txt"})\n'
            'second = await call_tool("read_file", {"file_path": "second.txt"})\n'
            'return {"first_chars": len(first["result"]), "second_chars": len(second["result"])}'
        )})
        self.assertEqual(result.data, {"first_chars": 5, "second_chars": 6})

    async def test_mounted_tool_available_through_execute(self):
        schema = await self.client.call_tool("get_schema", {"tools": ["computer_probe"]})
        self.assertIn("computer_probe", str(schema.content))
        result = await self.client.call_tool("execute", {
            "code": 'return await call_tool("computer_probe", {})'
        })
        self.assertIn("mounted", str(result.data))

    async def test_file_workspace_boundary_survives_code_mode(self):
        result = await self.client.call_tool("execute", {
            "code": 'return await call_tool("read_file", {"file_path": "../outside.txt"})'
        }, raise_on_error=False)
        self.assertTrue(result.is_error)


if __name__ == "__main__":
    unittest.main()
