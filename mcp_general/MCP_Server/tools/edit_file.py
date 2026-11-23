from ._paths import get_path
from ._atomic import atomic_write


def edit_file(file_path: str, old_text: str, new_text: str) -> str:
    """Replace exactly one occurrence in a UTF-8 workspace file."""
    if not old_text:
        raise ValueError("old_text cannot be empty.")
    path = get_path(file_path)
    with path.open(encoding="utf-8", newline="") as file:
        content = file.read()
    count = content.count(old_text)
    if count != 1:
        raise ValueError(f"Expected one match, found {count}.")
    atomic_write(path, content.replace(old_text, new_text, 1))
    return f"Updated: {path}"
