from typing import Callable

from pycodeowners._pycodeowners.models.owner import Owner, GitlabOwnerType
from pycodeowners._pycodeowners.models.parse_options.owner_matcher import (
    OwnerMatcher,
    usernameRegexp,
    groupRegexp,
    emailRegexp,
)


def match_gitlab_email_owner(s: str) -> Owner | None:
    match = emailRegexp.match(s)
    if match is None:
        return None

    return Owner(value=s, parsed_value=match.group(0), owner_type=GitlabOwnerType.EMAIL)


def match_gitlab_nested_group_owner(s: str) -> Owner | None:
    match = groupRegexp.match(s)
    if match is None:
        return None

    return Owner(
        value=s, parsed_value=match.group(1), owner_type=GitlabOwnerType.NESTED_GROUP
    )


def match_gitlab_group_or_username_owner(s: str) -> Owner | None:
    match = usernameRegexp.match(s)
    if match is None:
        return None

    return Owner(
        value=s,
        parsed_value=match.group(1),
        owner_type=GitlabOwnerType.GROUP_OR_USERNAME,
    )


class GitlabOwnerMatcher(OwnerMatcher):
    matchers: set[Callable[[str], Owner | None]] = {
        match_gitlab_email_owner,
        match_gitlab_nested_group_owner,
        match_gitlab_group_or_username_owner,
    }
