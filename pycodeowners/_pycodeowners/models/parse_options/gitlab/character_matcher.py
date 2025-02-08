from pycodeowners._pycodeowners.models.parse_options.character_matcher import (
    CharacterMatcher,
)


class GitlabCharacterMatcher(CharacterMatcher):
    @classmethod
    def is_valid_pattern_character(cls, char: str, is_escaped: bool) -> bool:
        if char == "#" and is_escaped:
            return True
        return super().is_valid_pattern_character(char, is_escaped)
