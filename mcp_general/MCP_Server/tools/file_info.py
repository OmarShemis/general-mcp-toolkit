from datetime import datetime, timezone

from ._paths import get_path


def file_info(file_path: str) -> dict:
    """Return a workspace entry's type, file size in bytes, and UTC modification time."""
    path = get_path(file_path)
    info = path.stat()
    return {
        "path": str(path),
        "type": "directory" if path.is_dir() else "file",
        "size_bytes": info.st_size if path.is_file() else None,
        "modified_at": datetime.fromtimestamp(info.st_mtime, timezone.utc).isoformat(),
        "is_symlink": path.is_symlink(),
    }
