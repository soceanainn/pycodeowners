from pycodeowners._pycodeowners.models.parse_options.character_matcher import (
    CharacterMatcher,
)


class BitbucketCharacterMatcher(CharacterMatcher):
    @classmethod
    def is_valid_owner_character(cls, char: str, is_escaped: bool) -> bool:
        if char in {"(", ")", ":"}:
            return True
        return super().is_valid_owner_character(char, is_escaped)
