import asyncio
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "MCP_Server"))

from tools._atomic import atomic_write
from tools._desktop_reliability import DesktopReliability, wait_seconds
from tools.edit_file import edit_file
from tools.write_file import write_file


class Files(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.environment = patch.dict(os.environ, MCP_WORKSPACE=self.directory.name)
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def test_edit_preserves_crlf_and_unicode(self):
        write_file("sample.txt", "first\r\nhello café\r\n")
        edit_file("sample.txt", "café", "world")
        self.assertEqual((Path(self.directory.name) / "sample.txt").read_bytes(),
                         b"first\r\nhello world\r\n")

    def test_replace_failure_preserves_original_and_removes_temp(self):
        target = Path(self.directory.name) / "sample.txt"
        target.write_text("original")
        with patch("tools._atomic.os.replace", side_effect=PermissionError("locked")):
            with self.assertRaises(PermissionError):
                atomic_write(target, "replacement")
        self.assertEqual(target.read_text(), "original")
        self.assertEqual(list(target.parent.iterdir()), [target])

    def test_ambiguous_edit_and_existing_write_leave_file_intact(self):
        write_file("sample.txt", "same same")
        with self.assertRaises(ValueError):
            edit_file("sample.txt", "same", "different")
        with self.assertRaises(FileExistsError):
            write_file("sample.txt", "replacement")
        self.assertEqual((Path(self.directory.name) / "sample.txt").read_text(), "same same")


class Desktop(unittest.IsolatedAsyncioTestCase):
    async def test_fractional_wait_and_validation(self):
        self.assertEqual(await wait_seconds(0.01), "Waited for 0.01 seconds.")
        for invalid in (-1, 61, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                await wait_seconds(invalid)

    async def test_interrupted_typing_is_not_replayed(self):
        attempts = 0
        async def interrupted(context):
            nonlocal attempts
            attempts += 1
            raise RuntimeError("CONTROL_PREEMPTED: ready")
        context = SimpleNamespace(message=SimpleNamespace(name="Type"))
        with self.assertRaisesRegex(Exception, "Do not replay"):
            await DesktopReliability().on_call_tool(context, interrupted)
        self.assertEqual(attempts, 1)

    async def test_other_failures_preserve_original_error(self):
        async def failed(context):
            raise ValueError("invalid location")
        context = SimpleNamespace(message=SimpleNamespace(name="Type"))
        with self.assertRaisesRegex(ValueError, "invalid location"):
            await DesktopReliability().on_call_tool(context, failed)


if __name__ == "__main__":
    unittest.main()
