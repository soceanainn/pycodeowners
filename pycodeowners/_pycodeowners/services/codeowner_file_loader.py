import subprocess
from pathlib import Path

from pycodeowners._pycodeowners.models.file_type import FileType
from pycodeowners._pycodeowners.models.parse_options import (
    GitlabParseOptions,
    BitBucketParseOptions,
)
from pycodeowners._pycodeowners.models.ruleset import Ruleset
from pycodeowners._pycodeowners.services.codeowner_file_parser import (
    CodeownerFileParser,
)


class CodeownerFileLoader:
    @classmethod
    def load(
        cls,
        path_and_type: tuple[str | Path, FileType] | None = None,
        file_parser: CodeownerFileParser | None = None,
    ) -> Ruleset:
        """loads and parses a CODEOWNERS file at the path specified.
        Checks standard locations for CODEOWNERS file if no path provided."""
        if path_and_type is not None:
            path, codeowner_type = path_and_type
        else:
            path, codeowner_type = cls._find_file_at_standard_location()

        if file_parser is None:
            match codeowner_type:
                case FileType.Github:
                    file_parser = CodeownerFileParser()
                case FileType.Gitlab:
                    file_parser = CodeownerFileParser(options=GitlabParseOptions())
                case FileType.BitBucket:
                    file_parser = CodeownerFileParser(options=BitBucketParseOptions())
                case _:
                    raise ValueError(
                        f"Unexpected value for codeowner file type: '{codeowner_type}'"
                    )

        with open(path) as f:
            return file_parser.parse(f)

    @classmethod
    def _find_file_at_standard_location(cls) -> tuple[Path, FileType]:
        """loops through the standard locations for
        CODEOWNERS files (.github/, ./, docs/, .gitlab/, .bitbucket/), and returns the first place a
        CODEOWNERS file is found, with an inferred FileType.
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
