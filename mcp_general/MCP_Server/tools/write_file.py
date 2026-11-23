from ._paths import get_path
from ._atomic import atomic_write


def write_file(file_path: str, content: str, overwrite: bool = False) -> str:
    """Write UTF-8 text within the workspace; replacing a file requires overwrite=True."""
    path = get_path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite:
        atomic_write(path, content)
    else:
        with path.open("x", encoding="utf-8", newline="") as file:
            file.write(content)
    return f"Saved: {path}"
