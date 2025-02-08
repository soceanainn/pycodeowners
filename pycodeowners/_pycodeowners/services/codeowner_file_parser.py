from typing import TextIO

from pycodeowners._pycodeowners.models.parse_options.character_matcher import (
    CharacterMatcherFunc,
)
from pycodeowners._pycodeowners.models.owner import Owner
from pycodeowners._pycodeowners.models.ruleset import Ruleset
from pycodeowners._pycodeowners.models.parse_options import (
    ParseOptions,
    GithubParseOptions,
)
from pycodeowners._pycodeowners.models.pattern import Pattern
from pycodeowners._pycodeowners.models.rule import Rule
from pycodeowners._pycodeowners.models.section import Section


class CodeownerFileParser:
    def __init__(self, options: ParseOptions = GithubParseOptions()) -> None:
        """To override the default owner and accepted character matchers, pass options parameter"""
        self.options = options

    def parse(
        self,
        file: TextIO,
    ) -> Ruleset:
        """parses a CODEOWNERS file, returning a set of rules."""

        ruleset = Ruleset()
        current_section: Section | None = None

        for line_num, line in enumerate(file, start=1):
            line = line.strip()

            # Ignore empty lines or lines only containing comments
            if line == "" or line[0] == "#":
                continue

            # For Gitlab, try to parse a new section heading, and skip parsing line as rule if found
            if line.startswith("[") or line.startswith("^[") and "]" in line:
                section = self._parse_gitlab_section_heading(line, line_num)
                if section is not None:
                    current_section = ruleset.get_or_create_section(section)
                    continue

            # Try to parse line as rule
            rule = self._parse_rule(line, line_num)

            # If in section, add rule to section, otherwise add to ruleset
            if current_section is not None:
                current_section.add_rule(rule)
            else:
                ruleset.add_rule(rule)

        return ruleset

    def _parse_gitlab_section_heading(
        self, section_str: str, line_num: int
    ) -> Section | None:
        require_approval = True
        if section_str.startswith("^"):
            require_approval = False
            section_str = section_str[2:]
        else:
            section_str = section_str[1:]

        section_name, last_seen_char = self._parse_token(
            section_str,
            line_num,
            character_matcher=self.options.character_matcher.is_valid_owner_character,
            termination_character="]",
        )

        if len(section_name) == 0 or last_seen_char == len(section_str) - 1:
            # If we reached end of line without a valid section name or a closing "]", return None and treat as standard rule (not section start)
            return None

        remaining_str = section_str[
            last_seen_char + 2 :
        ].strip()  # +2 to skip termination char ']'

        number_of_required_approvals: str | None = None
        if remaining_str.startswith("["):
            number_of_required_approvals, last_seen_char = self._parse_token(
                remaining_str,
                line_num,
                character_matcher=self.options.character_matcher.is_valid_owner_character,
                termination_character="]",
            )
            remaining_str = remaining_str[
                last_seen_char + 2 :
            ].strip()  # +2 to skip termination char ']'

        owners, comment = self._parse_owners(remaining_str, line_num)
        return Section(
            line_number=line_num,
            name=section_name,
            require_approval=require_approval,
            number_of_required_approvals=int(number_of_required_approvals)
            if number_of_required_approvals
            else None,
            default_owners=owners,
            comment=comment,
        )

    def _parse_owners(
        self, remaining_str: str, line_num: int
    ) -> tuple[list[Owner], str | None]:
        owners: list[Owner] = []
        while remaining_str:
            # Check for inline comments
            if remaining_str.startswith("#"):
                return owners, remaining_str

            # Read owners
            owner, last_seen_char = self._parse_token(
                remaining_str,
                line_num,
                character_matcher=self.options.character_matcher.is_valid_owner_character,
            )
            if owner:
                owners.append(self.options.owner_matchers.match(owner))
            remaining_str = remaining_str[last_seen_char + 1 :].strip()
        return owners, None

    def _parse_rule(self, rule_str: str, line_num: int) -> Rule:
        """parse_line parses a single line of a CODEOWNERS file, returning a Rule struct"""
        pattern_str, last_seen_char = self._parse_token(
            rule_str,
            line_num,
            character_matcher=self.options.character_matcher.is_valid_pattern_character,
        )

        if len(pattern_str) == 0:
            raise ValueError(f"Unexpected end of rule on line #{line_num}")

        remaining_str = rule_str[last_seen_char + 1 :].strip()

        owners, comment = self._parse_owners(remaining_str, line_num)

        return Rule(
            line_number=line_num,
            pattern=Pattern(pattern_str),
            owners=owners,
            comment=comment,
        )

    @classmethod
    def _parse_token(
        cls,
        line: str,
        line_num: int,
        character_matcher: CharacterMatcherFunc,
        termination_character: str | None = None,
    ) -> tuple[str, int]:
        buffered_string = ""
        escaped_character = False
        for idx, char in enumerate(line.strip()):
            if char == "\\":
                # Escape the next character but don't lose the backslash as it's part of the pattern
                escaped_character = True
                buffered_string += char

            elif not escaped_character and (
                (termination_character is None and char.isspace())
                or (char in {termination_character, "#"})
            ):
                # Unescaped termination character or '#' means the string we're parsing has ended
                # If termination character not set default to any whitespace string
                return buffered_string, idx - 1

            elif character_matcher(char, escaped_character):
                #  Keep any valid characters and escaped characters
                buffered_string += char
                escaped_character = False
            else:
                raise ValueError(
                    f"Received invalid character '{char}' on line #{line_num}"
                )
        return buffered_string, len(line) - 1
