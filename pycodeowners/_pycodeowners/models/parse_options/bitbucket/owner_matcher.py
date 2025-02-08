import re
from typing import Callable

from pycodeowners._pycodeowners.models.owner import (
    BitbucketOwnerType,
    BitbucketOwner,
    Owner,
)
from pycodeowners._pycodeowners.models.parse_options.owner_matcher import (
    OwnerMatcher,
)

emailRegexp = re.compile("^[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,6}$")
groupRegexp = re.compile("^@([a-zA-Z0-9-]+/[a-zA-Z0-9_-]+)(?::([A-Za-z0-9-_()]+))?$")
usernameRegexp = re.compile("^@([a-zA-Z0-9-_]+)(?:(:[A-Za-z0-9-_()]+))?$")


def match_bitbucket_email_owner(s: str) -> Owner | None:
    match = emailRegexp.match(s)
    if match is None:
        return None

    return Owner(
        value=s,
        parsed_value=s,
        owner_type=BitbucketOwnerType.EMAIL,
    )


def match_bitbucket_group_owner(s: str) -> Owner | None:
    match = groupRegexp.match(s)
    if match is None:
        return None

    return BitbucketOwner(
        value=s,
        parsed_value=match.group(1),
        owner_type=BitbucketOwnerType.GROUP,
        selection_strategy=match.group(2),
    )


def match_bitbucket_username_owner(s: str) -> Owner | None:
    match = usernameRegexp.match(s)
    if match is None:
        return None

    return BitbucketOwner(
        value=s,
        parsed_value=match.group(1),
        owner_type=BitbucketOwnerType.USERNAME,
        selection_strategy=match.group(2),
    )


class BitbucketOwnerMatcher(OwnerMatcher):
    matchers: set[Callable[[str], Owner | None]] = {
        match_bitbucket_email_owner,
        match_bitbucket_group_owner,
        match_bitbucket_username_owner,
    }
