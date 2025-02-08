import subprocess
from pathlib import Path

from pycodeowners._pycodeowners.models.file_type import FileType
from pycodeowners._pycodeowners.models.parse_options import (
    GitlabParseOptions,
    BitBucketParseOptions,
    GithubParseOptions,
    ParseOptions,
)


class CodeownerFileFinder:
    @classmethod
    def find(
        cls,
    ) -> tuple[Path, ParseOptions]:
        """Checks standard locations for CODEOWNERS file.
        Returns an inferred parse option based on the location of the CODEOWNERS file."""

        path, file_type = cls._find_file_at_standard_location()
        parse_options: ParseOptions
        match file_type:
            case FileType.Github:
                parse_options = GithubParseOptions()
            case FileType.Gitlab:
                parse_options = GitlabParseOptions()
            case FileType.BitBucket:
                parse_options = BitBucketParseOptions()
            case _:
                raise ValueError(
                    f"Unexpected value for codeowner file type: '{file_type}'"
                )
        return path, parse_options

    @classmethod
    def _find_file_at_standard_location(cls) -> tuple[Path, FileType]:
        """loops through the standard locations for
        CODEOWNERS files (.github/, ./, docs/, .gitlab/, .bitbucket/), and returns the first place a
        CODEOWNERS file is found, with an inferred FileParser.
        If run from a git repository, all paths are relative to the repository root."""
        path_prefix = Path(".")
        repo_root = cls._find_repository_root()
        if repo_root is not None:
            path_prefix = repo_root

        for path, file_type in {
            (".github/CODEOWNERS", FileType.Github),
            ("CODEOWNERS", FileType.Github),
            ("docs/CODEOWNERS", FileType.Github),
            (".gitlab/CODEOWNERS", FileType.Gitlab),
            (".bitbucket/CODEOWNERS", FileType.BitBucket),
        }:
            full_path = path_prefix / path

            if full_path.is_file():
                return full_path, file_type
        raise ValueError("Couldn't find CODEOWNERS file at a default location")

    @classmethod
    def _find_repository_root(cls) -> Path | None:
        """returns the path to the root of the git repository, if
        we're currently in one. If we're not in a git repository, the boolean return
         value is false."""
        completed_process = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], capture_output=True
        )
        if completed_process.returncode == 0 and completed_process.stdout:
            return Path(completed_process.stdout.decode("utf-8").strip())
        return None
