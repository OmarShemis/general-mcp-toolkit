import shutil

from ._paths import get_path, get_workspace


def delete(file_path: str, confirm: bool = False) -> str:
    """Permanently delete a workspace entry. confirm is a tool flag, not human approval."""
    path = get_path(file_path)
    if path.resolve() == get_workspace():
        raise ValueError("Cannot delete the workspace directory.")
    if not path.exists() and not path.is_symlink():
        raise FileNotFoundError(f"Path not found: {path}")
    if not confirm:
        return f"Set confirm=True to permanently delete: {path}"
    if path.is_symlink():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    return f"Deleted: {path}"
