import shutil

from ._paths import get_path


def copy_file(source: str, destination: str) -> str:
    """Copy a workspace file or folder. Destination must not exist; symbolic links are rejected."""
    source_path = get_path(source)
    destination_path = get_path(destination)
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    if destination_path.exists() or destination_path.is_symlink():
        raise FileExistsError(destination_path)
    if destination_path.resolve().is_relative_to(source_path.resolve()):
        raise ValueError("Cannot copy a folder into itself.")
    if source_path.is_symlink() or source_path.is_junction():
        raise ValueError("Copying symbolic links or junctions is not supported.")
    if source_path.is_dir():
        for path in source_path.rglob("*"):
            if path.is_symlink() or path.is_junction():
                raise ValueError(f"Folder contains a symbolic link or junction: {path}")
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    if source_path.is_dir():
        shutil.copytree(source_path, destination_path)
    else:
        with source_path.open("rb") as original, destination_path.open("xb") as copy:
            shutil.copyfileobj(original, copy)
    return f"Copied to: {destination_path}"
