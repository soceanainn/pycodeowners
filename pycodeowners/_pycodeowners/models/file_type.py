from enum import StrEnum, auto

from pycodeowners._pycodeowners.models.parse_options import (
    ParseOptions,
    BitbucketParseOptions,
    GitlabParseOptions,
    GithubParseOptions,
)


class FileType(StrEnum):
    Github = auto()
    Gitlab = auto()
    Bitbucket = auto()

    def get_default_parse_options(self) -> ParseOptions:
        match self:
            case FileType.Github:
                return GithubParseOptions()
            case FileType.Gitlab:
                return GitlabParseOptions()
            case FileType.Bitbucket:
                return BitbucketParseOptions()
