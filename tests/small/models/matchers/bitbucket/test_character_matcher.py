from pycodeowners._pycodeowners.models.parse_options.bitbucket.character_matcher import (
    BitbucketCharacterMatcher,
)


class TestIsValidOwnerCharacter:
    def test_supports_characters_supported_by_super_def(self) -> None:
        for char in {"a", "A", "á", "1"}:
            assert (
                BitbucketCharacterMatcher.is_valid_owner_character(char, False) is True
            )

    def test_returns_true_for_additional_supported_characters(self) -> None:
        for char in {"(", ")", ":"}:
            assert (
                BitbucketCharacterMatcher.is_valid_owner_character(char, False) is True
            )
