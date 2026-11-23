import subprocess
from tempfile import TemporaryFile

from ._paths import get_path


def run_command(
    command: list[str], directory: str = ".", timeout: int = 30,
    max_chars: int = 20_000,
) -> dict:
    """Run a program with separate arguments, without a shell. Commands have the server's OS permissions; the working directory is not a sandbox."""
    if not command or not command[0].strip():
        raise ValueError("command must contain a program and optional arguments.")
    if not 1 <= timeout <= 300:
        raise ValueError("timeout must be between 1 and 300 seconds.")
    if max_chars < 1:
        raise ValueError("max_chars must be positive.")
    with TemporaryFile() as stdout, TemporaryFile() as stderr:
        timed_out = False
        try:
            result = subprocess.run(
                command, cwd=get_path(directory), stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, timeout=timeout, shell=False,
            )
            returncode = result.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            returncode = None
        output = {}
        for name, stream in (("stdout", stdout), ("stderr", stderr)):
            stream.seek(0)
            text = stream.read(max_chars * 4 + 1).decode("utf-8", errors="replace")
            output[name] = text[:max_chars]
            output[f"{name}_truncated"] = len(text) > max_chars
        return {"returncode": returncode, "timed_out": timed_out, **output}
