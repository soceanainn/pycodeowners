from pathlib import Path

from pycodeowners import CodeownerFileParser
from pycodeowners._pycodeowners.cli_commands.arg_parsing import get_path_and_file_type
from pycodeowners._pycodeowners.models.file_type import FileType


def validate(file: Path | None, file_type: FileType | None, verbose: bool) -> None:
    path, file_type = get_path_and_file_type(file, file_type)

    file_parser = CodeownerFileParser(file_type.get_default_parse_options())
    with open(path, "r") as f:
        file_parser.parse(f)

    if verbose:
        print(f"{path} is valid")
