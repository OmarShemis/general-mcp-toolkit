from glob import iglob

from ._paths import get_path, get_workspace


def iter_files(pattern: str):
    """Yield matching workspace files; reject patterns or links outside the workspace."""
    if not pattern.strip():
        raise ValueError("pattern cannot be empty.")
    get_path(pattern)
    for name in iglob(pattern, root_dir=get_workspace(), recursive=True):
        path = get_path(name)
        if path.is_file():
            yield path


def find_files(pattern: str, max_results: int = 100) -> list[str]:
    """Find workspace files by glob pattern, such as **/*.py."""
    if max_results < 1:
        raise ValueError("max_results must be positive.")
    results = []
    for path in iter_files(pattern):
        results.append(str(path))
        if len(results) >= max_results:
            break
    return results
