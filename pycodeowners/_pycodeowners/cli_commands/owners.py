import os
from pathlib import Path

from pycodeowners._pycodeowners.cli_commands.arg_parsing import get_path_and_file_type
from pycodeowners._pycodeowners.models.file_type import FileType
from pycodeowners._pycodeowners.models.owner import OwnerType
from pycodeowners._pycodeowners.services.codeowner_file_parser import (
    CodeownerFileParser,
)


def owners(
    file: Path | None, file_type: FileType | None, verbose: bool, paths: list[Path]
) -> None:
    path, file_type = get_path_and_file_type(file, file_type)

    file_parser = CodeownerFileParser(file_type.get_default_parse_options())
    with open(path, "r") as f:
        ruleset = file_parser.parse(f)

    owners: set[tuple[str, OwnerType]] = set()

    max_owner_name_len: int = 0
    for owner in [owner for rule in ruleset.rules for owner in rule.owners]:
        max_owner_name_len = max(len(owner.parsed_value), max_owner_name_len)
        owners.add((owner.parsed_value, owner.owner_type))

    for section in ruleset.sections.values():
        for rule in section.rules:
            for owner in rule.owners:
                max_owner_name_len = max(len(owner.parsed_value), max_owner_name_len)
                owners.add((owner.parsed_value, owner.owner_type))

    max_display_len: int = max_owner_name_len
    try:
        terminal_size = os.get_terminal_size()[0]
    except OSError:
        pass  # not in terminal, e.g. called from tests
    else:
        max_display_len = min(max_owner_name_len, terminal_size) + 4

    for owner in owners:
        print(f"{owner[0]:{max_display_len}}({owner[1]})")
