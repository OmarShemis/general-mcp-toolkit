"""Local reliability adapters; never replay non-idempotent desktop input."""

import asyncio
import math

from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import Middleware


async def wait_seconds(duration: float) -> str:
    """Wait 0–60 seconds, including fractional seconds, without blocking the server."""
    if not math.isfinite(duration) or not 0 <= duration <= 60:
        raise ValueError("duration must be a finite number between 0 and 60 seconds.")
    await asyncio.sleep(duration)
    return f"Waited for {duration:g} seconds."


class DesktopReliability(Middleware):
    async def on_call_tool(self, context, call_next):
        try:
            return await call_next(context)
        except Exception as exc:
            if context.message.name == "Type" and "CONTROL_PREEMPTED" in str(exc):
                raise ToolError(
                    "CONTROL_PREEMPTED: typing may have partially completed. "
                    "Do not replay the text. Take a fresh Snapshot, inspect the "
                    "field, and resume only the missing text after control returns."
                ) from exc
            raise
