from typing import Callable

from pycodeowners._pycodeowners.models.owner import Owner, GithubOwnerType
from pycodeowners._pycodeowners.models.parse_options.owner_matcher import (
    OwnerMatcher,
    usernameRegexp,
    groupRegexp,
    emailRegexp,
)


def match_github_email_owner(s: str) -> Owner | None:
    match = emailRegexp.match(s)
    if match is None:
        return None

    return Owner(value=s, parsed_value=match.group(0), owner_type=GithubOwnerType.EMAIL)


def match_github_team_owner(s: str) -> Owner | None:
    match = groupRegexp.match(s)
    if match is None:
        return None

    return Owner(value=s, parsed_value=match.group(1), owner_type=GithubOwnerType.TEAM)


def match_github_username_owner(s: str) -> Owner | None:
    match = usernameRegexp.match(s)
    if match is None:
        return None

    return Owner(
        value=s, parsed_value=match.group(1), owner_type=GithubOwnerType.USERNAME
    )


class GithubOwnerMatcher(OwnerMatcher):
    matchers: set[Callable[[str], Owner | None]] = {
        match_github_email_owner,
        match_github_team_owner,
        match_github_username_owner,
    }
