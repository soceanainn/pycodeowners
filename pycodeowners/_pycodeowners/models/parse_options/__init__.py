from abc import ABC

from pycodeowners._pycodeowners.models.parse_options.bitbucket.character_matcher import (
    BitbucketCharacterMatcher,
)
from pycodeowners._pycodeowners.models.parse_options.bitbucket.owner_matcher import (
    BitbucketOwnerMatcher,
)
from pycodeowners._pycodeowners.models.parse_options.character_matcher import (
    CharacterMatcher,
)
from pycodeowners._pycodeowners.models.parse_options.github.owner_matcher import (
    GithubOwnerMatcher,
)
from pycodeowners._pycodeowners.models.parse_options.gitlab.character_matcher import (
    GitlabCharacterMatcher,
)
from pycodeowners._pycodeowners.models.parse_options.gitlab.owner_matcher import (
    GitlabOwnerMatcher,
)
from pycodeowners._pycodeowners.models.parse_options.owner_matcher import OwnerMatcher


class ParseOptions(ABC):
    character_matcher: CharacterMatcher
    owner_matchers: OwnerMatcher


class GithubParseOptions(ParseOptions):
    character_matcher = CharacterMatcher()
    owner_matchers = GithubOwnerMatcher()


class GitlabParseOptions(ParseOptions):
    character_matcher = GitlabCharacterMatcher()
    owner_matchers = GitlabOwnerMatcher()


class BitbucketParseOptions(ParseOptions):
    character_matcher = BitbucketCharacterMatcher()
    owner_matchers = BitbucketOwnerMatcher()
