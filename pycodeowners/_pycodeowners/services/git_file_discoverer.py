import subprocess
from pathlib import Path


class GitFileDiscoverer:
    @classmethod
    def discover(cls, input_paths: list[str] | None = None) -> list[Path]:
        default_args = ["git", "ls-files", "--others", "--exclude-standard"]
        if input_paths:
            default_args.extend(input_paths)
        else:
            default_args.extend(["."])
        res = subprocess.run(default_args, capture_output=True)
        if res.returncode != 0 or not res.stdout:
            raise RuntimeError("Failed to discover files")
        return [Path(filename) for filename in res.stdout.decode("utf-8").splitlines()]
