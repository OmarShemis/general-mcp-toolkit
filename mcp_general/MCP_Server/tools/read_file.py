from ._paths import get_path


def read_file(file_path: str, max_chars: int = 50_000) -> str:
    """Read UTF-8 text within the workspace, indicating truncated content."""
    if max_chars < 1:
        raise ValueError("max_chars must be positive.")
    with get_path(file_path).open(encoding="utf-8") as file:
        content = file.read(max_chars + 1)
    if len(content) > max_chars:
        return content[:max_chars] + "\n[Content truncated]"
    return content
