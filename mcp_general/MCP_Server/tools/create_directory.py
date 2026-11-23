from ._paths import get_path


def create_directory(directory: str) -> str:
    """Create a workspace directory and missing parents; existing directories are accepted."""
    path = get_path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return f"Directory ready: {path}"
