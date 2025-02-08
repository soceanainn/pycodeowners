from typing import Callable


class CharacterMatcher:
    @classmethod
    def is_valid_pattern_character(cls, char: str, is_escaped: bool) -> bool:
        return len(char) == 1 and (
            char.isalnum()
            or char in {"*", "?", ".", "/", "@", "_", "+", "-", "\\", "(", ")"}
            or (char.isspace() and is_escaped)
        )

    @classmethod
    def is_valid_owner_character(cls, char: str, is_escaped: bool) -> bool:
        return len(char) == 1 and (
            char.isalnum() or char in {".", "@", "/", "_", "%", "+", "-"}
        )


CharacterMatcherFunc = Callable[[str, bool], bool]
