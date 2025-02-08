import pytest

from pycodeowners._pycodeowners.models.parse_options.character_matcher import (
    CharacterMatcher,
)


class TestIsValidPatternCharacter:
    @pytest.mark.parametrize("is_escaped", [True, False])
    def test_returns_false_for_string_len_ne_1(self, is_escaped: bool) -> None:
        for char in {"", "ab"}:
            assert (
                CharacterMatcher.is_valid_pattern_character(char, is_escaped) is False
            )

    @pytest.mark.parametrize("is_escaped", [True, False])
    def test_returns_true_for_alphanumeric_chars(self, is_escaped: bool) -> None:
        for char in {"a", "A", "á", "1"}:
            assert CharacterMatcher.is_valid_pattern_character(char, is_escaped) is True

    @pytest.mark.parametrize("is_escaped", [True, False])
    def test_returns_true_for_allowed_special_chars(self, is_escaped: bool) -> None:
        for char in {"*", "?", ".", "/", "@", "_", "+", "-", "\\", "(", ")"}:
            assert CharacterMatcher.is_valid_pattern_character(char, is_escaped) is True

    def test_returns_true_for_escaped_whitespace(self) -> None:
        assert CharacterMatcher.is_valid_pattern_character(" ", True) is True

    def test_returns_false_for_non_escaped_whitespace(self) -> None:
        assert CharacterMatcher.is_valid_pattern_character(" ", False) is False


class TestIsValidOwnerCharacter:
    def test_returns_false_for_string_len_ne_1(self) -> None:
        for char in {"", "ab"}:
            assert CharacterMatcher.is_valid_owner_character(char, False) is False

    def test_returns_true_for_alphanumeric_chars(self) -> None:
        for char in {"a", "A", "á", "1"}:
            assert CharacterMatcher.is_valid_owner_character(char, False) is True

    def test_returns_true_for_allowed_special_chars(self) -> None:
        for char in {".", "@", "/", "_", "%", "+", "-"}:
            assert CharacterMatcher.is_valid_owner_character(char, False) is True
