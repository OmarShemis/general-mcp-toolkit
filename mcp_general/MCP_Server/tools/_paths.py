import os
from pathlib import Path


def get_workspace() -> Path:
    """Use MCP_WORKSPACE or the project directory as the workspace."""
    default = Path(__file__).resolve().parents[2]
    return Path(os.getenv("MCP_WORKSPACE", str(default))).expanduser().resolve()


def get_path(file_path: str) -> Path:
    """Resolve relative paths within the workspace and reject paths outside it."""
    workspace = get_workspace()
    path = Path(file_path).expanduser()
    if not path.is_absolute():
        path = workspace / path
    if not path.resolve().is_relative_to(workspace):
        raise ValueError("Path must stay inside the configured workspace.")
    return path.absolute()
