from dataclasses import dataclass, field
from pathlib import Path

from pycodeowners._pycodeowners.models.owner import Owner
from pycodeowners._pycodeowners.models.pattern import Pattern


@dataclass
class Rule:
    """Rule is a CODEOWNERS rule that maps a gitignore-style path pattern to a set of owners."""

    line_number: int
    owners: list[Owner] = field(default_factory=list)
    comment: str | None = None
    pattern: Pattern = field(init=False)

    def match(self, path: Path) -> bool:
        """match tests whether the provided Path matches the rule's pattern."""
        return self.pattern.match(path)
