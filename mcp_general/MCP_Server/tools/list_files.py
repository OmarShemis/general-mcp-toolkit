from ._paths import get_path


def list_files(directory: str = ".") -> list[str]:
    """List workspace directory entries; folders end with a slash."""
    path = get_path(directory)
    return sorted(item.name + ("/" if item.is_dir() else "") for item in path.iterdir())
