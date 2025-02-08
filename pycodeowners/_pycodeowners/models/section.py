from dataclasses import dataclass, field

from pycodeowners._pycodeowners.models.owner import Owner
from pycodeowners._pycodeowners.models.rule import Rule


@dataclass
class Section:
    line_number: int
    name: str
    require_approval: bool = True
    number_of_required_approvals: int | None = None
    default_owners: list[Owner] = field(default_factory=list)
    rules: list[Rule] = field(default_factory=list)
    comment: str | None = None

    def add_rule(self, rule: Rule) -> None:
        if not rule.owners:
            rule.owners = self.default_owners
        self.rules.append(rule)
