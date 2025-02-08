import re
from pathlib import Path

from pycodeowners._pycodeowners.services.regex_pattern_builder import (
    RegexPatternBuilder,
)


class Pattern:
    pattern: str
    regex: re.Pattern | None
    left_anchored_literal: bool

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
        if any(char in pattern for char in {"*", "?", "\\"}) and pattern[0] == "/":
            self.regex = None
            self.left_anchored_literal = True
        else:
            self.regex = RegexPatternBuilder.build(pattern)
            self.left_anchored_literal = False

    def match(self, test_path: Path) -> bool:
        path_str = str(test_path)

        if self.left_anchored_literal:
            prefix = self.pattern

            if prefix[0] == "/":
                # Strip the leading slash as we're anchored to the root already
                prefix = prefix[1:]

            if prefix[len(prefix) - 1] == "/":
                # If the pattern ends with a slash we can do a simple prefix match
                return path_str.startswith(prefix)

            if len(prefix) == len(path_str):
                # If the strings are the same length, check for an exact match
                return path_str == prefix

            if len(path_str) > len(prefix) and path_str[len(prefix)] == "/":
                # Check if the test path is a subdirectory of the pattern
                return path_str[: len(prefix)] == prefix

            # Otherwise the test path must be shorter than the pattern, so it can't match
            return False

        return self.regex.match(path_str) is not None  # type: ignore[union-attr]
