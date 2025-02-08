from dataclasses import dataclass
from enum import StrEnum, auto


class OwnerType(StrEnum):
    pass


class GithubOwnerType(OwnerType):
    # EMAIL is the owner type for email addresses.
    EMAIL = auto()
    # TEAM is the owner type for Github teams.
    TEAM = auto()
    # USERNAME is the owner type for Github usernames.
    USERNAME = auto()


class GitlabOwnerType(OwnerType):
    # EMAIL is the owner type for email addresses.
    EMAIL = auto()
    # NESTED_GROUP is the owner type for Gitlab nested groups.
    NESTED_GROUP = auto()
    # GROUP_OR_USERNAME is the owner type for Gitlab usernames or groups (which are indistinguishable from syntax).
    GROUP_OR_USERNAME = auto()


class BitbucketOwnerType(OwnerType):
    # EMAIL is the owner type for email addresses.
    EMAIL = auto()
    # GROUP is the owner type for Bitbucket groups.
    GROUP = auto()
    # USERNAME is the owner type for Bitbucket usernames.
    USERNAME = auto()


# Owner represents an owner found in a rule.
@dataclass
class Owner:
    owner_type: OwnerType
    value: str  # value is the original value in the CODEOWNER file
    parsed_value: str  # value is the parsed name of the owner


@dataclass
class BitbucketOwner(Owner):
    # Bitbucket has an additional selection strategy that may be applied
    selection_strategy: str | None = None
