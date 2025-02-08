import argparse
import re
import sys
import traceback
from pathlib import Path
from typing import Callable

from pycodeowners._pycodeowners.cli_commands.owners import owners
from pycodeowners._pycodeowners.cli_commands.file_owners import file_owners
from pycodeowners._pycodeowners.cli_commands.validate import validate
from pycodeowners._pycodeowners.models.errors import CodeownerSyntaxError
from pycodeowners._pycodeowners.models.file_type import FileType


class FormatterClass(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None) -> None:
        indent = " " * (self._indent_increment + self._current_indent)
        return super().add_usage(usage, actions, groups, prefix=f"Usage: \n{indent}")

    def start_section(self, heading: str) -> None:
        super().start_section(heading.capitalize())

    def _format_action_invocation(self, action):
        if isinstance(action, argparse._SubParsersAction):
            return ""
        return super()._format_action_invocation(action)

    def _format_action(self, action):
        format = super()._format_action(action)
        match = re.compile("^\\s*\n(.*)").match(format)
        if match:
            return match.group(1)
        return format


def help_wrapper[**P](parser: argparse.ArgumentParser) -> Callable[P, None]:
    def help(*args: P.args, **kwargs: P.kwargs) -> None:
        parser.print_help()

    return help


def main(*args: str) -> int:
    verbose_parent_parser = argparse.ArgumentParser(add_help=False)
    verbose_parent_parser.add_argument(
        "-v", "--verbose", action="store_true", default=argparse.SUPPRESS
    )

    codeowner_file_parent_parser = argparse.ArgumentParser(add_help=False)
    codeowner_file_parent_parser.add_argument("-f", "--file", default=None, type=Path)
    codeowner_file_parent_parser.add_argument(
        "-t", "--file-type", default=None, choices=FileType, type=FileType
    )

    owner_filter_parent_parser = argparse.ArgumentParser(add_help=False)
    owner_filter_parent_parser.add_argument(
        "-o", "--owner", nargs="*", default=[], type=str
    )
    owner_filter_parent_parser.add_argument(
        "-u", "--show-unowned", default=False, action="store_true"
    )

    parser = argparse.ArgumentParser(
        prog="pycodeowners", formatter_class=FormatterClass
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.set_defaults(func=help_wrapper(parser))

    subparsers = parser.add_subparsers(title="commands", metavar="<command>")

    validate_syntax_parser = subparsers.add_parser(
        "validate", parents=[codeowner_file_parent_parser, verbose_parent_parser]
    )
    validate_syntax_parser.set_defaults(func=validate)

    file_owners_parser = subparsers.add_parser(
        "files",
        help="Hello",
        parents=[
            codeowner_file_parent_parser,
            owner_filter_parent_parser,
            verbose_parent_parser,
        ],
    )
    file_owners_parser.add_argument("paths", nargs="*", default=[], type=Path)
    file_owners_parser.set_defaults(func=file_owners)

    owners_parser = subparsers.add_parser(
        "owners", parents=[codeowner_file_parent_parser, verbose_parent_parser]
    )
    owners_parser.add_argument("paths", nargs="*", default=[], type=Path)
    owners_parser.set_defaults(func=owners)

    args = vars(parser.parse_args(args))
    func = args.pop("func")
    verbose = args["verbose"]

    try:
        func(**args)
    except CodeownerSyntaxError as e:
        e.print(verbose)
        return 1

    except BaseException:
        print("pycodeowners encountered an unexpected error", file=sys.stderr)
        if verbose:
            print(traceback.format_exc(), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
