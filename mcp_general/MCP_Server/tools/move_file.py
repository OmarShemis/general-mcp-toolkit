import shutil

from ._paths import get_path, get_workspace


def move_file(source: str, destination: str) -> str:
    """Move or rename a workspace file or folder. Destination must not exist."""
    source_path = get_path(source)
    destination_path = get_path(destination)
    if source_path.resolve() == get_workspace():
        raise ValueError("Cannot move the workspace directory.")
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    if destination_path.exists() or destination_path.is_symlink():
        raise FileExistsError(destination_path)
    if destination_path.resolve().is_relative_to(source_path.resolve()):
        raise ValueError("Cannot move a folder into itself.")
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source_path), str(destination_path))
    return f"Moved to: {destination_path}"
