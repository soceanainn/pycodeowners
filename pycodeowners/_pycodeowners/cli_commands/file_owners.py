import os
from pathlib import Path

from pycodeowners._pycodeowners.cli_commands.arg_parsing import get_path_and_file_type
from pycodeowners._pycodeowners.models.file_type import FileType
from pycodeowners._pycodeowners.models.ruleset import Ruleset
from pycodeowners._pycodeowners.services.codeowner_file_parser import (
    CodeownerFileParser,
)
from pycodeowners._pycodeowners.services.git_file_discoverer import GitFileDiscoverer


def file_owners(
    file: Path | None,
    file_type: FileType | None,
    verbose: bool,
    owner: list[str] | None,
    show_unowned: bool,
    paths: list[str] | None,
) -> None:
    path, file_type = get_path_and_file_type(file, file_type)

    file_parser = CodeownerFileParser(file_type.get_default_parse_options())
    with open(path, "r") as f:
        ruleset = file_parser.parse(f)

    owner = [f.lstrip("@") for f in owner]

    if not paths or len(paths) == 0:
        paths = ["."]

    all_file_paths: list[Path] = GitFileDiscoverer.discover(paths)
    max_file_path_len: int = max(len(str(s)) for s in all_file_paths)

    max_display_len: int = max_file_path_len
    try:
        terminal_size = os.get_terminal_size()[0]
    except OSError:
        pass  # not in terminal, e.g. called from tests
    else:
        max_display_len = min(max_file_path_len, os.get_terminal_size()[0]) + 4

    for file_path in all_file_paths:
        print_file_owners(file_path, ruleset, owner, show_unowned, max_display_len)

    return


def print_file_owners(
    path: Path,
    ruleset: Ruleset,
    owner_filters: list[str],
    show_unowned: bool,
    width: int,
) -> None:
    rules = ruleset.match(path)

    matched_owners = [owner for rule in rules for owner in rule.owners]
    if not matched_owners:
        # If we didn't get a match, the file is unowned
        if not owner_filters or show_unowned:
            # Unless explicitly requested, don't show unowned files if we're filtering by owner
            print(f"{str(path):{width}}(unowned)")
        return

    owners_to_show: list[str] = []
    if not owner_filters:
        # If there are no filters, show all owners
        owners_to_show = [owner.value for owner in matched_owners]
    else:
        for owner in matched_owners:
            if owner.parsed_value in owner_filters:
                owners_to_show.append(owner.value)

    if owners_to_show:
        print(f"{str(path):{width}}" + (" ".join(owners_to_show)))
