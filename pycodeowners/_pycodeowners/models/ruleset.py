from dataclasses import dataclass, field
from pathlib import Path

from pycodeowners._pycodeowners.models.owner import Owner
from pycodeowners._pycodeowners.models.rule import Rule
from pycodeowners._pycodeowners.models.section import Section


@dataclass
class Ruleset:
    """Ruleset is a collection of CODEOWNERS rules, divided into sections.
    Rules defined outside of sections are implicitly considered to be a part of 'CODEOWNERS' section.
    While Gitlab is the only tool that actually supports sections, it's easier to just use this modelling for everything.
    """

    rules: list[Rule] = field(default_factory=list)
    sections: dict[str, Section] = field(default_factory=dict)

    def match(self, path: Path) -> list[Rule]:
        """match finds the last rule in the ruleset that matches the path provided. When
        determining the ownership of a file using CODEOWNERS, order matters, and the
        last matching rule takes precedence."""
        rules = []
        for rule in self.rules[::-1]:
            if rule.match(path):
                rules.append(rule)

        for section in self.sections.values():
            for rule in section.rules[::-1]:
                if rule.match(path):
                    rules.append(rule)
        return rules

    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)

    def get_default_owners_for_section(self, section_name: str) -> list[Owner]:
        return self.sections[section_name].default_owners

    def get_or_create_section(self, section: Section) -> Section:
        if section.name is None:
            raise ValueError("Cannot create section without name")
        section_key = section.name.lower()
        if section_key in self.sections:
            return self.sections[section_key]
        self.sections[section_key] = section
        return section
