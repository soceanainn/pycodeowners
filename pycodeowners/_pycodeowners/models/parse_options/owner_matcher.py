import re
from abc import ABC
from typing import Callable, TypeVar, Generic

from pycodeowners._pycodeowners.models.errors import InvalidOwnerError
from pycodeowners._pycodeowners.models.owner import Owner


emailRegexp = re.compile("^[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,6}$")
groupRegexp = re.compile("^@([a-zA-Z0-9-]+(/[a-zA-Z0-9_-]+)+)$")
usernameRegexp = re.compile("^@([a-zA-Z0-9-_]+)$")


OwnerT = TypeVar("OwnerT", bound=Owner, covariant=True)


class OwnerMatcher(Generic[OwnerT], ABC):
    matchers: set[Callable[[str], OwnerT | None]]

    @classmethod
    def match(cls, s: str) -> OwnerT:
        """match figures out which kind of owner s is and returns an Owner struct"""
        for owner_matcher in cls.matchers:
            o = owner_matcher(s)
            if o is not None:
                return o
        raise InvalidOwnerError("Invalid owner format: " + s)
