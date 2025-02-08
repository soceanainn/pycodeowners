from pathlib import Path

from pycodeowners import CodeownerFileFinder
from pycodeowners._pycodeowners.models.file_type import FileType


def get_path_and_file_type(
    path: str | None, file_type: FileType | None
) -> tuple[str | Path, FileType]:
    if path:
        inferred_file_type = FileType.Github
    else:
        path, inferred_file_type = CodeownerFileFinder.find()

    return path, file_type or inferred_file_type
