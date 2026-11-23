from .find_files import iter_files


def search_text(
    search_text: str, pattern: str = "**/*.py", max_results: int = 100,
) -> dict:
    """Search UTF-8 workspace files for literal text; report files that could not be read."""
    if not search_text:
        raise ValueError("search_text cannot be empty.")
    if max_results < 1:
        raise ValueError("max_results must be positive.")
    matches = []
    skipped = []
    for path in iter_files(pattern):
        try:
            with path.open(encoding="utf-8") as file:
                for number, line in enumerate(file, 1):
                    if search_text in line:
                        matches.append(f"{path}:{number}: {line.rstrip()}")
                        if len(matches) >= max_results:
                            return {"matches": matches, "skipped": skipped, "limit_reached": True}
        except (UnicodeError, OSError) as error:
            skipped.append({"path": str(path), "error": str(error)})
    return {"matches": matches, "skipped": skipped, "limit_reached": False}
