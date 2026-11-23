"""Commit replacements only after the entire UTF-8 file has been written."""

import os
from pathlib import Path
from tempfile import NamedTemporaryFile


def atomic_write(path: Path, content: str) -> None:
    temporary = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
