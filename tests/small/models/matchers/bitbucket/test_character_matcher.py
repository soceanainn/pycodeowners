from pycodeowners._pycodeowners.models.parse_options.bitbucket.character_matcher import (
    BitBucketCharacterMatcher,
)


class TestIsValidOwnerCharacter:
    def test_supports_characters_supported_by_super_def(self) -> None:
        for char in {"a", "A", "á", "1"}:
            assert (
                BitBucketCharacterMatcher.is_valid_owner_character(char, False) is True
            )

    def test_returns_true_for_additional_supported_characters(self) -> None:
        for char in {"(", ")", ":"}:
            assert (
                BitBucketCharacterMatcher.is_valid_owner_character(char, False) is True
            )
